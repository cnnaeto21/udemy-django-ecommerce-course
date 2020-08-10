form tags.models import tags


qs = Tag.objects.all()
print(qs)
black = Tag.objects.last()

black.title
black.slug

black.products


black.products.all()


black.products.all().first()

exit()