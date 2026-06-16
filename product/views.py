from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category, ProductImage, ProductReview
from .serializers import ProductSerializer, CreateCategorySerializer, ProductImageSerializer, ProductReviewSerializer, ProductCreateSerializer
from rest_framework.permissions import IsAdminUser


class ProductListAPIView(APIView):

    def get(self, request):

        slug_id = request.query_params.get("slug")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        is_new_arrivals = request.query_params.get("is_new_arrivals")
        search = request.query_params.get("search")

        include_inactive = request.query_params.get("all") == "true"
        if include_inactive:
            products = Product.objects.all().select_related("category")
        else:
            products = Product.objects.filter(is_active=True).select_related("category")

        if slug_id:
            products = products.filter(category__slug=slug_id)

        if start_date and end_date:
            products = products.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            )
        # Search Logic
        if search:

            products = products.filter(

                Q(name__icontains=search) |

                Q(description__icontains=search)

            )

        if is_new_arrivals:
            is_new_arrivals_bool = is_new_arrivals.lower() == 'true'
            products = products.filter(is_new_arrivals=is_new_arrivals_bool)

        serializer = ProductSerializer(products, many=True)

        serializer = ProductSerializer(products, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ProductDetailAPIView(APIView):

    def get(self, request, slug):

        try:
            product = Product.objects.select_related(
                "category"
            ).get(
                slug=slug,
                is_active=True
            )

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)

        return Response(serializer.data)


class ProductCreateAPIView(APIView):

    def post(self, request):

        serializer = ProductCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Product created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryCreateAPIView(APIView):

    def post(self, request):

        serializer = CreateCategorySerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Category created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryListAPIView(APIView):

    def get(self, request):

        categories = Category.objects.filter(
            is_active=True
        ).order_by("-id")

        serializer = CreateCategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


class ProductDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)


class DeleteCategoryAPIView(APIView):

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            category.delete()

            return Response(
                {"message": "Category deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ProductGalleryAddAPIView(APIView):
    """Upload one or more gallery images for a product (POST /api/products/<pk>/gallery/add/)"""

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist("images")
        if not files:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        for file in files:
            img_obj = ProductImage.objects.create(product=product, image=file)
            created.append(ProductImageSerializer(img_obj).data)

        return Response({"message": "Images uploaded successfully", "images": created}, status=status.HTTP_201_CREATED)


class ProductGalleryDeleteAPIView(APIView):
    """Delete a single gallery image by its ID (DELETE /api/products/gallery/<img_id>/delete/)"""

    def delete(self, request, img_id):
        try:
            img_obj = ProductImage.objects.get(pk=img_id)
        except ProductImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        img_obj.delete()
        return Response({"message": "Image deleted successfully"}, status=status.HTTP_200_OK)


class ProductReviewAddAPIView(APIView):
    """Add a review for a product (POST /api/products/<pk>/reviews/add/)"""

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(
                {
                    "message": "Review added successfully",
                    "review": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)