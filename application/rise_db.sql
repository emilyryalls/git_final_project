drop database rise_db;
create database rise_db;

use rise_db;

-- WORKOUT VIDEOS

-- goal table
create table goal
(
goal_id bigint not null primary key auto_increment,
fitness_goal varchar(100) not null
);

insert into goal(fitness_goal)
values
('Build muscle'),
('Improve stamina'),
('Lose weight'),
('Improve core strength');

select *
from goal;


-- experience table
create table experience
(
experience_id bigint not null primary key auto_increment,
user_experience varchar(30) not null
);

insert into experience(user_experience)
values
('Beginner'),
('Intermediate'),
('Advanced');

select *
from experience;


-- time table
-- time is a predefined data type in mysql so avoided using in the code below
create table workout_time
(
time_id bigint not null primary key auto_increment,
time_available varchar(30) not null
);

insert into workout_time(time_available)
values
('15 mins'),
('30 mins'),
('Over 30 mins');

select *
from workout_time;


-- workout video table
create table workout_video
(
video_id bigint not null primary key auto_increment,
video_name varchar(100) not null,
video_link varchar(300) not null,
goal_id bigint not null,
foreign key (goal_id) references goal(goal_id),
experience_id bigint not null,
foreign key (experience_id) references experience(experience_id),
time_id bigint not null,
foreign key (time_id) references workout_time(time_id)
);

insert into workout_video(video_name, video_link, goal_id, experience_id, time_id)
values
('Beginner Full Body Kettlebell Workout - 15 mins', 'https://www.youtube.com/watch?v=stx7PYeoMao', 1, 1, 1),
('Full Body Beginner Dumbbell Workout - 30 mins', 'https://www.youtube.com/watch?v=0yYiErHenzs', 1, 1, 2),
('Strength Workout with Weights - 40 mins', 'https://www.youtube.com/watch?v=MTF8-wuTH4Y', 1, 1, 3),
('Full Body Workout with Dumbbells - 15 mins', 'https://www.youtube.com/watch?v=2xPxOHXyBJk', 1, 2, 1),
('Full Body Dumbbell Workout - 30 mins', 'https://www.youtube.com/watch?v=GViX8riaHX4', 1, 2, 2),
('Full Body Strength Training - 45 mins', 'https://www.youtube.com/watch?v=_2CFlN4U5vM', 1, 2, 3),
('Dumbbell Arms & Shoulder Workout - 15 mins', 'https://www.youtube.com/watch?v=X6gWQ1Lcvjg', 1, 3, 1),
('Advanced Full Body Workout - 30 mins', 'https://www.youtube.com/watch?v=kbS0sRGfQFs', 1, 3, 2),
('Intense Strength Training Workout - 40 mins', 'https://www.youtube.com/watch?v=588-C4bEL28', 1, 3, 3),
('Beginner Cardio Workout - 15 mins', 'https://www.youtube.com/watch?v=VWj8ZxCxrYk', 2, 1, 1),
('Cardio Aerobics Workout - 30 mins', 'https://www.youtube.com/watch?v=vI5MzT-wIjs', 2, 1, 2),
('Aerobics for Beginners - 45 mins', 'https://www.youtube.com/watch?v=a44ayeoSfKM', 2, 1, 3),
('Standing Cardio Aerobics Workout - 15 mins', 'https://www.youtube.com/watch?v=v8CDptlpeys', 2, 2, 1),
('Cardio Workout at Home - 30 mins', 'https://www.youtube.com/watch?v=Yn0dV4s81H0', 2, 2, 2),
('Full Body Workout at Home - 1 hour', 'https://www.youtube.com/watch?v=d9DKVhHmZ2Y', 2, 2, 3),
('Sweaty HIIT Workout - 15 mins', 'https://www.youtube.com/watch?v=_3hoz1zATys', 2, 3, 1),
('Constant Cardio Workout - 30 mins', 'https://www.youtube.com/watch?v=p9GPq3g5IDQ', 2, 3, 2),
('Hardcore Full body HIIT Workout - 1 hour', 'https://www.youtube.com/watch?v=_fXF7LNpTrQ', 2, 3, 3),
('Full Body Beginner HIIT - 15 mins', 'https://www.youtube.com/watch?v=4UlxqqJcir0', 3, 1, 1),
('Full Body HIIT Workout for Beginners - 30 mins', 'https://www.youtube.com/watch?v=31G8WtwSj8c', 3, 1, 2),
('Full Body Workout at Home - 1 hour', 'https://www.youtube.com/watch?v=BHNtFY-MSnU', 3, 1, 3),
('Happy HIIT Workout - 15 mins', 'https://www.youtube.com/watch?v=oA-vJvJ_CtE', 3, 2, 1),
('Calorie Killer HIIT Workout - 35 mins', 'https://www.youtube.com/watch?v=9UQ60VlHiQ4', 3, 2, 2),
('Full Body Workout - 45 mins', 'https://www.youtube.com/watch?v=ILodiqpiUsc', 3, 2, 3),
('Killer HIIT Full Body Workout - 15 mins', 'https://www.youtube.com/watch?v=L0Ji6oTAovo', 3, 3, 1),
('High Intensity Full Body Workout - 30 mins', 'https://www.youtube.com/watch?v=aaU3U1hYAo4', 3, 3, 2),
('Super Sweaty HIIT Special - 1 hour', 'https://youtube.com/watch?v=yrNU9Q1XHYw', 3, 3, 3),
('Pilates Workout for Beginners - 15 mins', 'https://www.youtube.com/watch?v=tov0o3mi5h8', 4, 1, 1),
('Beginner Pilates at Home - 30 mins', 'https://www.youtube.com/watch?v=2mkR5LPhOC4', 4, 1, 2),
('Full Body Pilates Workout for Beginners - 45 mins', 'https://www.youtube.com/watch?v=2e0byzM5zkQ', 4, 1, 3),
('Intermediate Pilates Full Body Workout - 15 mins', 'https://www.youtube.com/watch?v=QwrpxRJqdWE', 4, 2, 1),
('Full Body Intermediate Pilates Workout - 30 mins', 'https://www.youtube.com/watch?v=ZeutqUI8Btg', 4, 2, 2),
('At-Home Pilates Full Body Workout - 45 mins', 'https://www.youtube.com/watch?v=dN5fWO9m1AY', 4, 2, 3),
('Toning Full Body Pilates Workout - 15 mins', 'https://www.youtube.com/watch?v=mXXvpYYQDMc', 4, 3, 1),
('Full Body Pilates Workout - 30 mins', 'https://www.youtube.com/watch?v=8Ro7ScpYP1E', 4, 3, 2),
('Advanced Pilates Workout - 45 mins', 'https://www.youtube.com/watch?v=pPbPUAEr1ZY', 4, 3, 3);


select *
from workout_video;


-- join tables to make a view for workout videos
create view v_workout_videos
as
select
	v.video_name,
	v.video_link,
	g.fitness_goal as 'fitness_goal',
    e.user_experience as 'experience',
    t.time_available as 'time'
from workout_video as v
JOIN
goal as g
on v.goal_id = g.goal_id
JOIN
experience as e
on v.experience_id = e.experience_id
JOIN
workout_time as t
on v.time_id = t.time_id;

select *
from v_workout_videos;


-- MEAL PLAN

-- diet table
create table diet
(
diet_id bigint not null primary key auto_increment,
dietary_requirement varchar(30) not null
);

insert into diet(dietary_requirement)
values
('Vegan'),
('No preference');

select *
from diet;

-- meal plan table
create table meal_plan
(
meal_plan_id bigint not null primary key auto_increment,
image_link varchar(300) not null,
diet_id bigint not null,
foreign key (diet_id) references diet(diet_id),
goal_id bigint not null,
foreign key (goal_id) references goal(goal_id)
);

select *
from meal_plan;


-- MEMBERS

-- email table
create table email
(
email_id bigint not null primary key auto_increment,
email_address varchar(250) not null unique
);

select *
from email;

-- member table
create table member
(
member_id bigint not null primary key auto_increment,
first_name varchar(50) not null,
last_name varchar(100) not null,
email_id bigint not null,
foreign key (email_id) references email(email_id),
date_of_birth date null,
height decimal(5,2),
weight decimal(5,2),
goal_id bigint null,
foreign key (goal_id) references goal(goal_id),
diet_id bigint null,
foreign key (diet_id) references diet(diet_id),
profile_pic varchar(500)
);


-- password table
create table member_password
(
password_id bigint not null primary key auto_increment,
member_id bigint not null,
hashed_password text not null,
foreign key (member_id) references member(member_id)
);

-- newsletter table
create table newsletter
(
newsletter_id bigint not null primary key auto_increment,
email_id bigint not null,
foreign key (email_id) references email(email_id)
);

-- login view for internal code only
create view v_login_details
as
select
	m.member_id,
	m.first_name,
	e.email_address,
    p.hashed_password
from email as e
JOIN
member as m
on m.email_id = e.email_id
JOIN
member_password as p
on p.member_id = m.member_id;

select *
from member;