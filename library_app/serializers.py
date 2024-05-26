# from rest_framework import serializers
# from library_app.models import Author, Genre, Book, BookReservation, BooksBorrow
#
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'
#
#
# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = '__all__'
#
#
# class BookSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer(read_only=True)
#     genre = GenreSerializer(read_only=True)
#
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#
# class BookDetailSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer(read_only=True)
#     genre = GenreSerializer(read_only=True)
#
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#
# class BookCreateSerializer(serializers.ModelSerializer):
#     author = serializers.CharField(max_length=100)
#     genre = serializers.CharField(max_length=100)
#
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#     def create(self, validated_data):
#         author_name = validated_data.pop('author')
#         genre_name = validated_data.pop('genre')
#
#         author, _ = Author.objects.get_or_create(name=author_name)
#         genre, _ = Genre.objects.get_or_create(name=genre_name)
#
#         validated_data['author'] = author
#         validated_data['genre'] = genre
#
#         return Book.objects.create(**validated_data)
#
#
# class BookUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'
#
#
# class BookReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookReservation
#         fields = '__all__'
#
#
# class BookReservationCreateSerializer(serializers.ModelSerializer):
#     book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.filter(stock_quantity__gt=0))
#
#     class Meta:
#         model = BookReservation
#         fields = ['book']
#
#
# class BooksBorrowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BooksBorrow
#         fields = '__all__'
#
#
# class AvailableBookTitleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'title']
#
#
# class TopBooksSerializer(serializers.Serializer):
#     book_title = serializers.CharField()
#     times_borrowed = serializers.IntegerField()
#
#
# class LateReturnBooksSerializer(serializers.Serializer):
#     book_title = serializers.CharField()
#     late_returns_count = serializers.IntegerField()
#
#
# class LateReturnUsersSerializer(serializers.Serializer):
#     user_email = serializers.EmailField()
#     late_returns_count = serializers.IntegerField()

from rest_framework import serializers
from library_app.models import Author, Genre, Book, BookReservation, BooksBorrow


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=100)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        author_name = validated_data.pop("author")
        genre_name = validated_data.pop("genre")

        author, _ = Author.objects.get_or_create(name=author_name)
        genre, _ = Genre.objects.get_or_create(name=genre_name)

        validated_data["author"] = author
        validated_data["genre"] = genre

        return Book.objects.create(**validated_data)


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReservation
        fields = "__all__"


class BookReservationCreateSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(stock_quantity__gt=0)
    )

    class Meta:
        model = BookReservation
        fields = ["book"]


class BooksBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBorrow
        fields = "__all__"


class AvailableBookTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]


class TopBooksSerializer(serializers.Serializer):
    title = serializers.CharField()
    times_borrowed = serializers.IntegerField()


class LateReturnBooksSerializer(serializers.Serializer):
    title = serializers.CharField()
    late_returns_count = serializers.IntegerField()


class LateReturnUsersSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    late_returns_count = serializers.IntegerField()
