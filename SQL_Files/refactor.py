files = ['ER_2_Award.sql', 'ER_2_Critic.sql', 'ER_2_Movie_Genre.sql', 'ER_2_Movie_List.sql', 'ER_2_Movie.sql', 'ER_2_Person_ActsIn_Movie.sql', 'ER_2_Person_ActsIn_TV_Episode.sql', 'ER_2_Person_Directs_Movie.sql', 'ER_2_Person_Directs_TV_Episode.sql', 'ER_2_Person_Phone.sql', 'ER_2_Person.sql', 'ER_2_Person_Writes_Movie.sql', 'ER_2_Person_Writes_TV_Episode.sql', 'ER_2_Production_House.sql', 'ER_2_TV_Episode.sql', 'ER_2_TV_Series_genre.sql', 'ER_2_TV_Series_List.sql', 'ER_2_TV_Series.sql', 'ER_2_User_Follows_User.sql', 'ER_2_User_Rates_Movie.sql', 'ER_2_User_Rates_TV_Episodes.sql', 'ER_2_User_Rates_TV_Series.sql', 'ER_2_User_Reviews_Movie.sql', 'ER_2_User_Reviews_TV_Episode.sql', 'ER_2_User_Reviews_TV_Series.sql', 'ER_2_User.sql']

di = './data-sync/'
di2 = './population-files/'

for f in files:

    with open(di + f, 'r') as sql_file:

        outName = f
        outName = outName.replace('ER_2_', 'Movie_Master_')
        sql_file_o = open(di2 + outName, 'w')

        queries = sql_file.read().split(';')

        for query in queries:

            changed_query = query.replace('`ER-2`', '`movie-master`', 1)
            sql_file_o.write(changed_query + ';')

        sql_file_o.close()

    print("🎉🎉  Done with " + f)




