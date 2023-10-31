import ast
import numpy as np
import base64
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from gensim.models import Word2Vec

from .models import SessionList, WordVector
from .serializers import SessionListSerializer
from .permissions import ReadOnlyPermission
from .Feature.verifyToken import VerifyToken


class SessionListViewSet(viewsets.ModelViewSet):
    queryset = SessionList.objects.all()
    serializer_class = SessionListSerializer
    permission_classes = [ReadOnlyPermission]


class TrainWord2VecAPIView(APIView):
    def post(self, request):
        getToken = request.data.get('token')
        checkRole = VerifyToken.decode_token(getToken)

        if checkRole:
            purchases_train = []
            sessionList = SessionList.objects.all()
            for i in sessionList:
                purchases_train.append(i.listCodeProduct)

            # Đào tạo mô hình Word2Vec
            model = Word2Vec(window=10, sg=1, hs=0,
                             negative=10,  # for negative sampling
                             alpha=0.03, min_alpha=0.0007,
                             seed=14)

            model.build_vocab(purchases_train, progress_per=200)

            model.train(purchases_train, total_examples=model.corpus_count,
                        epochs=10, report_delay=1)

            # Lưu mô hình vào cơ sở dữ liệu
            for word in model.wv.index_to_key:
                vector = model.wv[word]

                # Chuyển đổi vector thành chuỗi Base64
                vector_base64 = base64.b64encode(vector.tobytes()).decode('utf-8')

                word_vector, created = WordVector.objects.get_or_create(codeProduct=word)
                word_vector.vector = vector_base64
                word_vector.save()

            return Response({'message': 'Train lại bộ gợi ý thành công'},
                            status=status.HTTP_200_OK)

        return Response({'message': 'Bạn không đủ quyền'},
                        status=status.HTTP_403_FORBIDDEN)


class GetListCodeProductView(APIView):
    def post(self, request):
        # Nhận request danh sách
        text_data = request.data.get('product-view')
        sessionProducts = ast.literal_eval(text_data)

        # Lấy giá trị đã train ở đb
        word_vectors = WordVector.objects.all()

        # Chuyển sang dạng nhị phân rồi sang  NumPy
        words = [entry.codeProduct for entry in word_vectors]
        vectors = [np.frombuffer(base64.b64decode(entry.vector), dtype=np.float32) for entry in word_vectors]

        vectors = [np.frombuffer(vector, dtype=np.float32) for vector in vectors]
        model = Word2Vec(sentences=words, window=10, sg=1, hs=0,
                         negative=10, alpha=0.03, min_alpha=0.0007, seed=14)

        model.wv[words] = vectors
        model.init_sims(replace=True)

        # Liệt kê san phẩm gợi ý
        def similar_products(v, n=6):
            ms = model.wv.most_similar([v], topn=n + 1)

            new_ms = []
            for j in ms:
                print(j)
                new_ms.append(j[0])

            return new_ms

        # Tính vector trung bình
        def aggregate_vectors(products):
            product_vec = []
            for i in products:
                try:
                    product_vec.append(model.wv.get_vector(i))
                except KeyError:
                    continue
            # Tính giá trị trung bình
            return np.mean(product_vec, axis=0)

        listSuggest = similar_products(aggregate_vectors(sessionProducts))
        return Response({'message': listSuggest}, status=status.HTTP_200_OK)
