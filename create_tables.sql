create table `movie-master`.Production_House
(
    Name  varchar(100) not null
        primary key,
    Email varchar(100) not null
);


create table `movie-master`.Movie
(
    ID                    int          not null
        primary key,
    Title                 varchar(100) not null,
    Duration              int          null comment 'In minutes
',
    Lang                  varchar(100) null,
    Description           varchar(200) null,
    Release_Year          year         null,
    Production_House_Name varchar(100) not null,
    constraint Movie_Production_House_Name_fk
        foreign key (Production_House_Name) references `movie-master`.Production_House (Name)
            on update cascade on delete cascade,
    check (Duration >= 0)
);
create table `movie-master`.TV_Series
(
    ID                    int          not null
        primary key,
    Title                 varchar(100) null,
    Lang                  varchar(100) null,
    Start_Year            year         null,
    End_Year              year         null,
    Production_House_Name varchar(100) null,
    constraint TV_Series_Production_House_Name_fk
        foreign key (Production_House_Name) references `movie-master`.Production_House (Name),

        check ((End_Year is null) or Start_Year <= End_Year)
);


create table `movie-master`.Person
(
    ID          int          not null
        primary key,
    Name        varchar(100) null,
    Sex         varchar(100) null,
    DOB         varchar(10)  null,
    Nationality varchar(100) null,
    Email       varchar(100) null,
    check ( Sex in  ('Male','Female')  )

);

create table `movie-master`.Award
(
    Name         varchar(100) not null,
    Category     varchar(100) not null,
    Year         year         not null,
    Person_ID    int          null,
    Movie_ID     int          null,
    TV_Series_ID int          null,
    primary key (Name, Category, Year),
     CHECK ((Not(Award.Person_ID is null and Award.Movie_ID is null and Award.TV_Series_ID is null)) AND (NOT(Award.TV_Series_ID is not null and Award.Movie_ID is not null))),
    constraint Award_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on delete cascade,
    constraint Award_Person_ID_fk
        foreign key (Person_ID) references `movie-master`.Person (ID)
            on delete cascade,
    constraint Award_TV_Series_ID_fk
        foreign key (TV_Series_ID) references `movie-master`.TV_Series (ID)
            on delete cascade
);

create table `movie-master`.User
(
    UserName varchar(100) not null
        primary key,
    Email    varchar(100) not null,
    constraint User_Email_uindex
        unique (Email)
);
create table `movie-master`.Critic
(
    UserName varchar(100) not null
        primary key,
    Email    varchar(100) null,
    Sex      varchar(100) not null,
    Name     varchar(100) not null,
    age      int          null,
    constraint Critic_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);



create table `movie-master`.Movie_List
(
    UserName varchar(100) not null,
    ListName varchar(100) not null,
    Movie_ID int          not null,
    primary key (UserName, ListName, Movie_ID),
    constraint Movie_List_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint Movie_List_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);

create table `movie-master`.TV_Series_List
(
    UserName     varchar(100) not null,
    ListName     varchar(100) not null,
    TV_series_ID int          not null,
    primary key (UserName, ListName, TV_series_ID),
    constraint TV_Series_List_TV_Series_ID_fk
        foreign key (TV_series_ID) references `movie-master`.TV_Series (ID)
            on update cascade on delete cascade,
    constraint TV_Series_List_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);


create table `movie-master`.Person_ActsIn_Movie
(
    Person_ID int not null,
    Movie_ID  int not null,
    primary key (Person_ID, Movie_ID),
    constraint Person_ActsIn_Movie_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint Person_ActsIn_Movie_ibfk_1
        foreign key (Person_ID) references `movie-master`.Person (ID)
            on update cascade on delete cascade
);


create table `movie-master`.TV_Episode
(
    ID             int          not null,
    Title          varchar(100) null,
    Duration       int          null,
    Lang           varchar(100) null,
    Description    varchar(100) null,
    Season_Number  int          null,
    Episode_Number int          null,
    Series_ID      int          not null,
    primary key (ID, Series_ID),
    constraint TV_Episode_TV_Series_ID_fk
        foreign key (Series_ID) references `movie-master`.TV_Series (ID)
            on update cascade on delete cascade
);



create table `movie-master`.`Person_ActsIn_TV-Episode`
(
    Person_ID     int not null,
    TV_Episode_ID int not null,
    TV_series_ID  int not null,
    primary key (Person_ID, TV_Episode_ID, TV_series_ID),
    constraint `Person_ActsIn_TV-Episode_Person_ID_fk`
        foreign key (Person_ID) references `movie-master`.Person (ID),
    constraint `Person_ActsIn_TV-Episode_TV_Episode_ID_fk`
        foreign key (TV_Episode_ID) references `movie-master`.TV_Episode (ID),
    constraint `Person_ActsIn_TV-Episode_TV_Series_ID_fk`
        foreign key (TV_series_ID) references `movie-master`.TV_Series (ID)
);

create table `movie-master`.Person_Directs_Movie
(
    Person_ID int not null,
    Movie_ID  int not null,
    primary key (Person_ID, Movie_ID),
    constraint Person_Directs_Movie_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint Person_Directs_Movie_ibfk_1
        foreign key (Person_ID) references `movie-master`.Person (ID)
            on update cascade on delete cascade
);

create table `movie-master`.`Person_Directs_TV-Episode`
(
    Person_ID     int not null,
    TV_Episode_ID int not null,
    TV_Series_ID  int not null,
    primary key (Person_ID, TV_Episode_ID, TV_Series_ID),
    constraint `Person_Directs_TV-Episode_Person_ID_fk`
        foreign key (Person_ID) references `movie-master`.Person (ID),
    constraint `Person_Directs_TV-Episode_TV_Episode_ID_fk`
        foreign key (TV_Episode_ID) references `movie-master`.TV_Episode (ID),
    constraint `Person_Directs_TV-Episode_TV_Episode_Series_ID_fk`
        foreign key (TV_Series_ID) references `movie-master`.TV_Episode (Series_ID)
);

create table `movie-master`.Person_Writes_Movie
(
    Person_ID int not null,
    Movie_ID  int not null,
    primary key (Person_ID, Movie_ID),
    constraint Person_Writes_Movie_Movie_ID_fk_2
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint Person_Writes_Movie_ibfk_1
        foreign key (Person_ID) references `movie-master`.Person (ID)
            on update cascade on delete cascade
);


create table `movie-master`.`Person_Writes_TV-Episode`
(
    Person_ID     int not null,
    TV_Episode_ID int not null,
    TV_Series_ID  int not null,
    primary key (Person_ID, TV_Episode_ID, TV_Series_ID),
    constraint `Person_Writes_TV-Episode_Person_ID_fk`
        foreign key (Person_ID) references `movie-master`.Person (ID),
    constraint `Person_Writes_TV-Episode_TV_Episode_ID_fk`
        foreign key (TV_Episode_ID) references `movie-master`.TV_Episode (ID),
    constraint `Person_Writes_TV-Episode_TV_Episode_Series_ID_fk`
        foreign key (TV_Series_ID) references `movie-master`.TV_Episode (Series_ID)
);


create table `movie-master`.Person_Phone
(
    Person_ID    int         not null
        primary key,
    Number       varchar(15) not null,
    Country_Code int         not null,
    constraint Person_Phone_Person_ID_fk
        foreign key (Person_ID) references `movie-master`.Person (ID)
);





create table `movie-master`.User_Follows_User
(
    UserName1 varchar(100) not null,
    UserName2 varchar(100) not null,
    primary key (UserName1, UserName2),
    constraint User_Follows_User_User_UserName_fk
        foreign key (UserName1) references `movie-master`.User (UserName)
            on update cascade on delete cascade,
    constraint User_Follows_User_User_UserName_fk_2
        foreign key (UserName2) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);

create table `movie-master`.User_Rates_Movie
(
    UserName varchar(100) not null,
    Movie_ID int          not null,
    Rating   float        not null,
    primary key (UserName, Movie_ID),
    constraint User_Rates_Movie_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint User_Rates_Movie_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade,
    check( Rating>=0 AND Rating<= 10 )
);
create table `movie-master`.User_Rates_TV_Episodes
(
    UserName      varchar(100) not null,
    TV_Episode_ID int          not null,
    Rating        float        not null,
    primary key (UserName, TV_Episode_ID),
    constraint User_Rates_TV_Episodes_TV_Episode_ID_fk
        foreign key (TV_Episode_ID) references `movie-master`.TV_Episode (ID)
            on update cascade on delete cascade,
    constraint User_Rates_TV_Episodes_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName),
    check( Rating>=0 AND Rating<= 10 )


);

create table `movie-master`.User_Rates_TV_Series
(
    UserName     varchar(100) not null,
    TV_Series_ID int          not null,
    Rating       float        not null,
    primary key (UserName, TV_Series_ID),
    constraint User_Rates_TV_Series_TV_Series_ID_fk
        foreign key (TV_Series_ID) references `movie-master`.TV_Series (ID)
            on update cascade on delete cascade,
    constraint User_Rates_TV_Series_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade,
    check( Rating>=0 AND Rating<= 10 )

);

create table `movie-master`.User_Reviews_Movie
(
    UserName varchar(100)  not null,
    Movie_ID int           not null,
    Text     varchar(5000) not null,
    Date     varchar(100)  not null,
    primary key (UserName, Movie_ID),
    constraint User_Reviews_Movie_Movie_ID_fk
        foreign key (Movie_ID) references `movie-master`.Movie (ID)
            on update cascade on delete cascade,
    constraint User_Reviews_Movie_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);

create table `movie-master`.User_Reviews_TV_Episode
(
    UserName      varchar(100)  not null,
    TV_Episode_ID int           not null,
    Text          varchar(5000) not null,
    Date          date          not null,
    primary key (UserName, TV_Episode_ID),
    constraint User_Reviews_TV_Episode_TV_Episode_ID_fk
        foreign key (TV_Episode_ID) references `movie-master`.TV_Episode (ID)
            on update cascade on delete cascade,
    constraint User_Reviews_TV_Episode_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);

create table `movie-master`.User_Reviews_TV_Series
(
    UserName     varchar(100)  not null,
    TV_Series_ID int           not null,
    Text         varchar(5000) not null,
    Date         varchar(100)  not null,
    primary key (UserName, TV_Series_ID),
    constraint User_Reviews_TV_Series_TV_Series_ID_fk
        foreign key (TV_Series_ID) references `movie-master`.TV_Series (ID)
            on update cascade on delete cascade,
    constraint User_Reviews_TV_Series_User_UserName_fk
        foreign key (UserName) references `movie-master`.User (UserName)
            on update cascade on delete cascade
);

