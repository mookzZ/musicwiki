from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from .models import Group, Album, Song, GroupMember

def home(request):
    latest_groups = Group.objects.all().order_by('-created_at')[:5]  # Последние 5 групп
    latest_albums = Album.objects.all().order_by('-release_date')[:5]  # Последние 5 альбомов
    latest_songs = Song.objects.all().order_by('-id')[:5]  # Последние 5 песен

    return render(request, 'home.html', {
        'latest_groups': latest_groups,
        'latest_albums': latest_albums,
        'latest_songs': latest_songs,
    })


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    albums = group.albums.all()
    songs = group.songs.all()
    return render(request, 'group_detail.html', {'group': group, 'albums': albums, 'songs': songs})

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    songs = album.songs.all()
    return render(request, 'album_detail.html', {'album': album, 'songs': songs})

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'song_detail.html', {'song': song})

def member_detail(request, pk):
    member = get_object_or_404(GroupMember, pk=pk)
    return render(request, 'member_detail.html', {'member': member})





def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups_list.html', {'groups': groups})

def album_list(request):
    albums = Album.objects.all()  # Получаем все альбомы
    return render(request, 'albums_list.html', {'albums': albums})

def song_list(request):
    songs = Song.objects.all()  # Получаем все треки
    return render(request, 'songs_list.html', {'songs': songs})

def group_member_list(request):
    members = GroupMember.objects.all()  # Получаем всех участников
    return render(request, 'group_members_list.html', {'members': members})

def search_view(request):
    query = request.GET.get("q", "").strip()  # Убираем пробелы
    results = {
        "groups": [],
        "albums": [],
        "songs": [],
        "members": [],
    }

    if query:
        results["groups"] = Group.objects.filter(Q(name__icontains=query))
        results["albums"] = Album.objects.filter(Q(name__icontains=query))
        results["songs"] = Song.objects.filter(Q(name__icontains=query))
        results["members"] = GroupMember.objects.filter(Q(name__icontains=query))

    # Формируем кликабельные ссылки
    for key, queryset in results.items():
        for obj in queryset:
            obj.url = reverse(f"{key[:-1]}_detail", args=[obj.pk])

    return render(request, "search_results.html", {"results": results, "query": query})
