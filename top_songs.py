import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import base64
import urllib


#Making an cover image for playlist
def cover_image_creation(year,month,name,profile_photo,URI):
    #Downloading spotify code
    page="https://scannables.scdn.co/uri/plain/png/DE8CCC/white/550/spotify:playlist:"+URI
    m=0
    fd = urllib.request.urlopen(profile_photo)
    fc = urllib.request.urlopen(page)
    spotify_code=Image.open(fc)
    photo=Image.open(fd)
    color_palette=[[[222,140,204],[233,83,152],[236,19,118]]]
    img = Image.new('RGB', (1000,1000),color=(color_palette[m][0][0],color_palette[m][0][1],color_palette[m][0][2]))
    d=ImageDraw.Draw(img)

    fnt1 = ImageFont.truetype('C:/Windows/Fonts/Tahoma/tahoma.ttf', 50)
    d.text((175,30),str(name),font=fnt1,fill=(color_palette[m][1][0],color_palette[m][1][1],color_palette[m][1][2]))
    fnt = ImageFont.truetype('C:/Windows/Fonts/Tahoma/tahoma.ttf', 200)
    d.text((75,250),month,font=fnt,fill=(color_palette[m][1][0],color_palette[m][1][1],color_palette[m][1][2]))
    fnt = ImageFont.truetype('C:/Windows/Fonts/seguihis.ttf', 400)
    d.text((75,400),year,font=fnt,fill=(color_palette[m][2][0],color_palette[m][2][1],color_palette[m][2][2]),spacing=5)
    photo.thumbnail((75,75), Image.ANTIALIAS)
    photo.convert("RGB")  

    #Pasting profile picture
    bigsize=(photo.size[0], photo.size[1])
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(photo.size, Image.ANTIALIAS)
    output = ImageOps.fit(photo, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('profile_circle.png')

    img.paste(output,(75,25),output)
    img.paste(spotify_code,(75,850))
    img.save('playlist_cover.png')

#Change your ID and SECRET_ID
ID=<ID>
SECRET_ID=<SECRET_ID>
URI = "https://example.com"
scope="playlist-modify-private playlist-modify-public user-top-read ugc-image-upload"

now = datetime.datetime.now()
year= now.year
month= now.strftime("%m")
monthPL=["Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]
name="Moje ulubione piosenki "+ monthPL[int(month)-1] + " " + str(year)
description="Stworzono: "+str(now.day)+" "+ monthPL[int(month)-1] + " " + str(year)

auto = SpotifyOAuth(ID,SECRET_ID,URI,scope=scope)
spt = spotipy.Spotify(auth_manager=auto)
user=spt.me()['id']

popular_song=spt.current_user_top_tracks(limit=50,time_range='short_term')

#Creating song list
song_list=[]
for song in popular_song['items']:
    song_list.append(song['id'])

created_playlist=spt.user_playlist_create(user=user,name=name,public=True)
playlist_id=created_playlist['id']
cover_image_creation(year=str(year),month=monthPL[int(month)-1],name=spt.me()['display_name'],profile_photo=spt.me()['images'][0]['url'],URI=playlist_id)

spt.playlist_add_items(playlist_id=playlist_id,items=song_list)

with open('playlist_cover.png', 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')

spt.playlist_upload_cover_image(playlist_id=playlist_id, image_b64=base64_message)

spt.playlist_change_details(playlist_id=playlist_id, name=None, public=None, collaborative=None, description=description)
