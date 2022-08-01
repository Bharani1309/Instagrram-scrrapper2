import instaloader
from urllib.parse import urlparse
import os
import csv
from datetime import date, datetime, timedelta

bot = instaloader.Instaloader()

file_name = os.getcwd() + "/list.csv"
file_name2 = os.getcwd() + "/final.csv"

rows_arr=[]
suggested_profiles_list=[]

with open(file_name, 'r', newline='', encoding="utf8", errors='ignore') as csvfile:
 reader = csv.DictReader(csvfile)
 
 for rows in reader:
   
   url = rows['SuggestedProfile']
   rp = rows['ReferredProfile']
   st = rows['Status']
   phrases = ['limited edition', 'edition print', 'giclee', 'giclée', 'c-type', 'archival', 'fine art print', 'buy print', 'print shop', 'print store', 'print catalog', 'nft', 'print', 'art', 'fine art', 'art print', 'print store', 'open edition', 'museum grade', 'museum quality', "print collection", "cotton rag", "acid free", "acid-free", "aquarelle", "hahnemühle", "hahnemuhle", "canson", "photorag", 'museum standard', 'gallery grade', 'gallery quality', 'gallery standard', 'cotton rag', 'gsm', 'reproductions', 'certificate', 'authenticity', 'authenticated', 'signature', 'signed', 'hand signed', 'framed']
   aud_phrases = ['artist', 'photographer', 'illustrator', 'patreon', 'kickstarter', 'etsy', 'discord', 'shop', 'masterclass', 'workshop', 'course', 'tutorial', 'presets']
   n_phrases = ['screen print', "aluminium", "perspex", "dibond", "mounted", "canvas", 'cafepress', 'redbubble', 'society6', 'zazzle', 'inprnt', 'roomfifty', 'fineartamerica', 'gold leaf']
   
   parsed_url_path = urlparse(url).path.replace("/", "")
   print(parsed_url_path)
   profile = instaloader.Profile.from_username(bot.context, parsed_url_path) if st == "New Lead" else ""
   
   profile_followers = profile.followers if st == "New Lead" else 0
   profile_followees = profile.followees if st == "New Lead" else 0
   profile_external_url = profile.external_url if st == "New Lead" else ""
   profile_bio = profile.biography if st == "New Lead" else ""
   post_keywords = [i for i in phrases if i in profile_bio.lower()] if st == "New Lead" else ""
   audience_keywords = [i for i in aud_phrases if i in profile_bio.lower()] if st == "New Lead" else ""
   negative_keywords = [i for i in n_phrases if i in profile_bio.lower()] if st == "New Lead" else ""
   st = "Bad Lead" if int(profile_followers) < 5000 and st == "New Lead" else st
   post_data = profile.get_posts() if st == "New Lead" else lambda: iter(())
   
   try:
    for i, posts in enumerate(post_data):
       today = datetime.today()
       
       post_date = (posts.date)
       if post_date <= today or post_date >= today:
        if posts.caption and len(posts.caption)>0:
         post = posts.caption.lower()
         print(post)
         print(i)
         p_k = [i for i in phrases if i in post]
         a_k = [i for i in aud_phrases if i in post]
         n_k = [i for i in n_phrases if i in post]
         post_keywords = (post_keywords + list(set(p_k) - set(post_keywords)))
         audience_keywords = (audience_keywords + list(set(a_k) - set(audience_keywords)))
         negative_keywords = (negative_keywords + list(set(n_k) - set(negative_keywords))) 
         print(post_keywords) 
       else:
        break
   except:
     print("unable to load")
      
      
     

     
   rows_arr.append({'InstagramLeads': "https://www.instagram.com/"+parsed_url_path, 'FollowersCount': profile_followers, 'FolloweesCount': profile_followees, 'Website_URL': profile_external_url, 'Bio': profile_bio, 'IG Post Keywords': ",".join(post_keywords), 'IG Audience Keywords': ",".join(audience_keywords),'IG Negative Keywords':",".join(negative_keywords), 'ReferredProfile': rp, 'Status': st})
   with open(file_name2, 'a', newline='', encoding="utf8", errors='ignore') as csvfile:
    fieldnames = ['InstagramLeads','FollowersCount','FolloweesCount','Website_URL','Bio','IG Post Keywords','IG Audience Keywords','IG Negative Keywords','ReferredProfile','Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  
    for item in rows_arr:
     writer.writerow(item)
    rows_arr=[]

with open(file_name, 'w', newline='', encoding="utf8", errors='ignore') as csvfile:
    fieldnames = ['InstagramLeads','FollowersCount','FolloweesCount','Website_URL','Bio','IG Post Keywords','IG Audience Keywords','IG Negative Keywords','ReferredProfile','Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in rows_arr:
     writer.writerow(item)
   
   
   





