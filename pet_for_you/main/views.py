from django.shortcuts import render


def main(request):
    context = dict(
        title='Главная страница'
    )
    return render(request, 'main/index.html', context=context)