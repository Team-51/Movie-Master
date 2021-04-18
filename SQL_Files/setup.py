from mysql.connector import connect
from dotenv import load_dotenv
import os
import traceback
import copy

load_dotenv()

conf = {
    'host': os.getenv('MYSQL_HOST') or 'localhost',
    'user': os.getenv('MYSQL_USER') or '',
    'password': os.getenv('MYSQL_PASSWORD') or 'password'
}
db_name = '`movie-master`'
create_sql_path = './create_tables.sql'

files = ['ER_2_User.sql', 'ER_2_Award.sql', 'ER_2_Critic.sql', 'ER_2_Movie_Genre.sql', 'ER_2_Movie_List.sql', 'ER_2_Movie.sql', 'ER_2_Person_ActsIn_Movie.sql', 'ER_2_Person_ActsIn_TV_Episode.sql', 'ER_2_Person_Directs_Movie.sql', 'ER_2_Person_Directs_TV_Episode.sql', 'ER_2_Person_Phone.sql', 'ER_2_Person.sql', 'ER_2_Person_Writes_Movie.sql', 'ER_2_Person_Writes_TV_Episode.sql', 'ER_2_Production_House.sql', 'ER_2_TV_Episode.sql', 'ER_2_TV_Series_genre.sql', 'ER_2_TV_Series_List.sql', 'ER_2_TV_Series.sql', 'ER_2_User_Follows_User.sql', 'ER_2_User_Rates_Movie.sql', 'ER_2_User_Rates_TV_Episodes.sql', 'ER_2_User_Rates_TV_Series.sql', 'ER_2_User_Reviews_Movie.sql', 'ER_2_User_Reviews_TV_Episode.sql', 'ER_2_User_Reviews_TV_Series.sql']

di = './population-files/'

def setup(cu, db):

    print(f"\n🧹🧼 Cleaning up existing database 🧼🧹\n")
    
    q = f'DROP SCHEMA IF EXISTS {db_name};'

    try:
        cu.execute(q)
        db.commit()

    except Exception:
        print("No drop...")

    print(f"\n✨💥 Creating new database 💥✨")
    
    try:
        cu.execute(f'CREATE SCHEMA IF NOT EXISTS {db_name};')
        db.commit()
        cu.execute(f'USE {db_name};')
        db.commit()

    except Exception:
        print(f'Continuing ...')

    cu.close()
    cu = db.cursor()
    try:
        with open(create_sql_path, 'r') as sql_file:
            queries =  sql_file.read().split(';')
            for query in queries:
                q = f'{query.strip()};'
                if len(q) <= 1:
                    continue
                cu.execute(f'{query};')
                db.commit()
                cu.close()
                cu = db.cursor()
            
            
    except Exception as e:
        print(f'Error: {e}')
        print("Could not create database.\nCan not proceed\nExiting...")
        exit(1)
    
    print(f"\n🎉🎉 Setup complete. Starting population 🎉🎉\n")

def populate(cu, db):
    
    cu.close()
    cu = db.cursor()

    dic = {}
    for f in files:

        outName = f
        outName = outName.replace('ER_2_', 'Movie_Master_')
        dic[outName] = 1


    while len(dic) > 0:

        dic2 = copy.deepcopy(dic)

        for f in dic.keys():
            
            with open(di + f, 'r') as sql_file:

                if 'Person' not in f:
                    queries = sql_file.read().splitlines()
                else: 
                    queries = sql_file.read().split(';')

                success = True

                for query in queries:

                    q = f'{query.strip()};'
                    if len(q) <= 1:
                        continue

                    if len(query) < 5:
                        continue

                    try:
                        cu.execute(f'{query}')

                    except: 
                        if 'Review' in f or 'List' in f or 'Rates' in f or 'Award' in f or 'Critic':
                            continue
                        print(query, f)
                        traceback.print_exc()
                        success = False
                        break

                if success:
                    db.commit()
                    del dic2[f]
                    print(f"Done with {f}")
                else:
                    db.rollback()

                cu.close()
                cu = db.cursor()

        dic = copy.deepcopy(dic2)

if __name__ == '__main__':

    db = connect(**conf)
    cu = db.cursor()
    setup(cu, db)
    populate(cu, db)


