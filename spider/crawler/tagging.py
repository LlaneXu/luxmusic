# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-29 23:13
@Author  : Lei Xu
@Email   : Llane_xu@outlook.com
@File    : tagging.py

Description:

Update:

Todo:


"""
# system import

# 3rd import

# self import

# module level variables here

# Create your models here.
"""
tag list:

album        -- name of the set this work belongs to
album_artist -- main creator of the set/album, if different from artist.
                e.g. "Various Artists" for compilation albums.
artist       -- main creator of the work
comment      -- any additional description of the file.
composer     -- who composed the work, if different from artist.
copyright    -- name of copyright holder.
creation_time-- date when the file was created, preferably in ISO 8601.
date         -- date when the work was created, preferably in ISO 8601.
disc         -- number of a subset, e.g. disc in a multi-disc collection.
encoder      -- name/settings of the software/hardware that produced the file.
encoded_by   -- person/group who created the file.
filename     -- original name of the file.
genre        -- <self-evident>.
language     -- main language in which the work is performed, preferably
                in ISO 639-2 format. Multiple languages can be specified by
                separating them with commas.
performer    -- artist who performed the work, if different from artist.
                E.g for "Also sprach Zarathustra", artist would be "Richard
                Strauss" and performer "London Philharmonic Orchestra".
publisher    -- name of the label/publisher.
service_name     -- name of the service in broadcasting (channel name).
service_provider -- name of the service provider in broadcasting.
title        -- name of the work.
track        -- number of this work in the set, can be in form current/total.
variant_bitrate -- the total bitrate of the bitrate variant that the current stream is part of

"title"	Name	'\251nam'
"author"	Artist	'\251ART'
"album_artist"	Album Artist	'aART'
"album"	Album	'\251alb'
"grouping"	Grouping	'\251grp'
"composer"	Composer	'\251wrt'
"year"	Year	'\251day'
"track"	Track Number	'trkn'
"comment"	Comments	'\251cmt'
"genre"	Genre	'\251gen'
"copyright"	??	'\251cpy'
"description"	Description	'desc'
"synopsis"	Information dialog when selecting "Show Description" in context menu	'ldes'
"show"	Show	'tvsh'
"episode_id"	Episode ID	'tven'
"network"	??	'tvnn'
"lyrics"	Lyrics	'\251lyr'

cmd
ffmpeg -i ~/Downloads/2.m4a \
 -metadata artist="陈奕迅" \
 -metadata title="富士山下" \
 -metadata year="2015" \
 -metadata genre="Hip-Hop" \
 -metadata lyrics="this is lyrics yes something" \
 -acodec copy \
 -y ~/Downloads/3.m4a

"""