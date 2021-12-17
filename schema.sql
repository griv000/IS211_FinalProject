DROP TABLE IF EXISTS tblUsers;
DROP TABLE IF EXISTS tblBlogPosts;
DROP TABLE IF EXISTS tblCategories;

CREATE TABLE tblUsers (
    UserID INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    UserLogin TEXT,
    UserPass TEXT,
    BlogTitle TEXT,
    LoginStatus TEXT
    );

CREATE TABLE tblBlogPosts (
    BlogID INTEGER PRIMARY KEY,
    PostTitle TEXT,
    PostContent TEXT,
    UserIDRef INTEGER,
    PublishDate DATE,
    PublishStatus TEXT,
    CategoryIDRef INTEGER
    );

CREATE TABLE tblCategories (
    CategoryID INTEGER PRIMARY KEY,
    UserIDRef INTEGER,
    CategoryName TEXT
);

INSERT INTO tblUsers VALUES 
    (1,'George','Washington','gwashington','america','From the Desk of the President','False'),
    (2,'Thomas','Edison','tedison','electric','My New Invention','False')
    ;

INSERT INTO tblBlogPosts VALUES
    (1,"Hello World","Discipline is the soul of an army. It makes small numbers formidable; procures success to the weak, and esteem to all.",1,'2020-01-02',"ACTIVE",1),
    (2,"2nd post","Liberty, when it begins to take root, is a plant of rapid growth.",1,'2020-02-02',"INACTIVE",2),
    (3,"My Thoughts","We often miss opportunity because it's dressed in overalls and looks like work",2,'2019-01-23',"ACTIVE",3),
    (4,"More thoughts","The three great essentials to achieve anything worthwhile are, first, hard work; second, stick-to-itiveness; third, common sense",2,'2018-01-02',"INACTIVE",4)
    ;

INSERT INTO tblCategories VALUES
    (1,1,"America"),
    (2,1,"President"),
    (3,2,"Electric"),
    (4,2,"Discoveries")
    ;