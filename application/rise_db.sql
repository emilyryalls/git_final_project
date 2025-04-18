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
('Low Impact Cardio Workout - 30 mins', 'https://www.youtube.com/watch?v=ImI63BUUPwU', 2, 1, 2),
('Walking Workout - 1 hour', 'https://www.youtube.com/watch?v=VWDnBWyKZ1Y', 2, 1, 3),
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
('Super Sweaty HIIT Special - 1 hour', 'https://www.youtube.com/watch?v=yrNU9Q1XHYw', 3, 3, 3),
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

INSERT INTO email (email_id, email_address) VALUES (1, 'zara.smith@example.com');

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
experience_id bigint,
foreign key (experience_id) references experience(experience_id),
profile_pic varchar(500),
member_since timestamp default current_timestamp
);

INSERT INTO member (first_name, last_name, email_id, date_of_birth, height, weight, goal_id, diet_id, experience_id, profile_pic)
VALUES ('Zara', 'Smith', 1, '1995-08-12', 165.00, 60.50, 1, 1, 1, 'static/images/zara.jpeg'
);

select *
from member;


-- password table
create table member_password
(
password_id bigint not null primary key auto_increment,
member_id bigint not null,
hashed_password text not null,
foreign key (member_id) references member(member_id) on delete cascade
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

    -- BLOG --

CREATE TABLE blog_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO blog_category (category)
VALUES
('Workout Routines'),
('Nutrition'),
('Mindset & Motivation'),
('Weight Loss'),
('Fitness for Beginners'),
('Recovery & Injury Prevention'),
('Health & Wellness'),
('Fitness Challenges');


CREATE TABLE blog_author (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO blog_author (author_name)
VALUES
('Reanna'),
('Emily'),
('Sakeena'),
('Ivon');


CREATE TABLE blog (
    blog_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author_id INT NOT NULL,
    image VARCHAR(500) NOT NULL,
    summary VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES blog_author(author_id),
    FOREIGN KEY (category_id) REFERENCES blog_category(category_id)
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'The Power of Consistency in Your Workout Routine',
    '1',
    'images/blog_img/blog1.jpg',
    'Consistency is the cornerstone of success in fitness. In this post, we’ll explore why making exercise a part of your daily routine is the key to lasting results.',
    'One of the biggest misconceptions in fitness is that you need to work out intensely for hours every single day to achieve results. While it’s true that consistency is critical, it doesn’t have to come with grueling intensity every time. The real power lies in showing up day after day and staying committed, even on the days when motivation is low. Whether you’re a beginner or an advanced fitness enthusiast, creating and sticking to a consistent workout routine will transform your body and mind over time.
Why Consistency Is More Important Than Intensity It’s tempting to think that the harder you push yourself, the faster you’ll see results. But what’s often overlooked is the fact that our bodies need time to adapt to new exercises. Intense workouts might burn a lot of calories in the short term, but without consistency, those results will be fleeting. In contrast, small, consistent efforts build sustainable progress that sticks.
The key is to set realistic goals that you can incorporate into your daily life. Whether that’s committing to exercise 3-4 times a week, or making small changes like taking the stairs instead of the elevator, consistency compounds over time. In fact, regular, moderate activity is more effective in achieving long-term health than sporadic bursts of high-intensity exercise.
Building a Sustainable Routine The first step in building a consistent workout routine is identifying what works for you. If you dread early-morning gym sessions, then don’t force yourself to work out at 6 a.m. Instead, schedule your workouts for a time when you feel your best, whether that’s during lunch, after work, or in the evening.
Consistency also means developing a habit. When you integrate workouts into your daily schedule, they become a part of your lifestyle. Think of exercise as brushing your teeth—something you just do every day. It won’t feel like a chore if it becomes a non-negotiable part of your routine.
One great strategy is to plan your week ahead. Write down your workout days, and treat them like appointments you can’t miss. Over time, you’ll start to look forward to these sessions rather than dreading them. If you miss a day, don’t sweat it. Just get back on track the next day, and don’t let guilt derail your progress.
The Role of Accountability Another way to stay consistent is by making your workouts social. Find a workout buddy or join a fitness group. Not only will this make your workouts more enjoyable, but it’ll also keep you accountable. When someone else is counting on you, you’re less likely to skip your sessions. In the age of social media, sharing your fitness journey with others can also be a powerful motivator. Post updates, progress photos, and celebrate small victories together.
Mindset Is Key Consistency in fitness doesn’t just apply to physical effort; it’s also about maintaining a strong mindset. There will be days when you feel tired, frustrated, or unmotivated. On these days, remind yourself why you started your fitness journey. Whether it’s to feel more energetic, lose weight, or improve your overall health, revisiting your “why” can help reignite your drive.
Focus on the journey rather than the destination. Fitness is a lifelong pursuit, not a race. Don’t let setbacks discourage you. Instead, use them as learning experiences. Remember, the journey is just as important as the destination—and it’s the small steps you take every day that will ultimately get you to where you want to be.
Consistency Involves More Than Just Exercise Consistency also applies to your nutrition, sleep, and recovery. If you’re working hard in the gym but neglecting recovery or eating poorly, your progress will stall. Make sure you’re getting enough rest and fueling your body with the proper nutrients. Consistency in these areas will enhance your performance in the gym and support your recovery.
The Takeaway Fitness isn’t about perfection; it’s about consistency. Embrace the small, steady changes you’re making, and let that momentum build over time. Set manageable goals, stick to a routine, and stay positive. As you begin to see improvements in your fitness, you’ll realize that the hard work and consistency were worth it. Remember, Rome wasn’t built in a day, and neither will your body. But with time, effort, and consistency, the results will speak for themselves.
Key Takeaways:
Consistency is the secret to long-term success.
Build a routine that works for you, not against you.
Stay accountable and positive through the highs and lows.',
    '1'
);


INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Nutrition 101: How to Fuel Your Body for Optimal Performance',
    '2',
    'images/blog_img/blog2.jpg',
    'Proper nutrition is essential for fueling your body, supporting muscle growth, and enhancing performance. This blog breaks down how to fuel your workouts and recovery to maximize your results.',
    'In the world of fitness, there’s a saying that’s as true as it gets: “You can’t out-train a bad diet.” No matter how hard you work at the gym, your body won’t perform at its best without the proper fuel. Your muscles need a combination of macronutrients—proteins, carbohydrates, and fats—to perform well during your workouts and recover effectively after. Let’s dive into the science behind nutrition and how you can apply it to achieve your fitness goals.
The Basics of Macronutrients: Your body requires three main macronutrients: protein, carbohydrates, and fats. Each one plays a crucial role in supporting various aspects of your workout routine, from providing energy to helping your muscles recover. Understanding how each of these nutrients works can help you optimize your diet for peak performance.
Protein: Protein is the building block of muscles. Without it, your body cannot repair or grow muscle fibers after exercise. When you lift weights or engage in intense activity, your muscles sustain tiny tears that need to be repaired. Protein does this job by providing the necessary amino acids to rebuild muscle tissue. Aim to include high-quality protein sources like lean meats (chicken, turkey), fish (salmon, tuna), and plant-based proteins (tofu, quinoa, lentils) in every meal.
How much protein do you need? That depends on your fitness goals. A good rule of thumb is to consume about 1.2 to 2.0 grams of protein per kilogram of body weight, especially if you’re focusing on building muscle.
Carbohydrates: Carbs are your body’s primary source of energy, especially when it comes to high-intensity workouts. Think of carbs as the fuel in your body’s engine. Complex carbohydrates, such as whole grains, vegetables, and fruits, are great because they release energy slowly, allowing for sustained performance. Simple carbs, on the other hand, provide quick energy, but they don’t keep you fueled for long.
Before your workout, aim to consume a small serving of complex carbs like oats, sweet potatoes, or brown rice. Afterward, eating a mix of carbs and protein helps replenish glycogen stores and repair muscle damage.
Fats: Fats often get a bad reputation, but they’re essential for hormone production and cellular health. They also help your body absorb fat-soluble vitamins (A, D, E, and K), which are critical for bone health, immune function, and overall well-being. Include healthy fats like avocado, nuts, seeds, and olive oil in your diet, and don’t shy away from them. Your body needs them for optimal performance.
Micronutrients Matter Too In addition to macronutrients, your body also needs a variety of vitamins and minerals to function properly. Micronutrients don’t provide energy, but they play a role in energy production, muscle contraction, immune function, and injury recovery. Make sure to eat a colorful array of fruits and vegetables to cover your micronutrient needs. Leafy greens, berries, citrus fruits, and nuts are all excellent sources.
Hydration is Key Water is essential for every cell in your body. Staying hydrated during your workout ensures your muscles have the fluid they need to function properly. Dehydration can impair performance, reduce strength, and lead to quicker fatigue. It’s not just about drinking water while you’re working out—it’s important to stay hydrated throughout the day.
Timing Your Nutrition Meal timing is another important factor. Pre-workout nutrition provides your body with the energy needed to perform at your best, while post-workout nutrition helps your muscles recover and grow. Ideally, you should eat a balanced meal 1-2 hours before your workout and follow it up with a meal containing both protein and carbohydrates within 30-60 minutes after your session.
Key Takeaways:
Protein is essential for muscle repair and growth.
Carbohydrates fuel your workouts, while fats support hormone production.
Hydration and micronutrients are crucial for optimal performance.
Timing your meals around your workouts boosts recovery and results.',
    '2'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Boost Your Motivation: How to Stay Driven During Your Fitness Journey',
    '3',
    'images/blog_img/blog3.jpg',
    'Staying motivated on your fitness journey can be challenging. In this blog, we dive into the psychology of motivation and provide actionable tips to help you stay driven through every high and low of your fitness journey.',
    'Motivation is often described as the fuel that drives your fitness journey. But anyone who’s been on the fitness path for a while knows that motivation is fickle. There are days when it’s easy to hit the gym and crush your goals, and there are other days when you feel like you can’t get off the couch. If you’ve ever struggled with motivation, you’re not alone—and there are proven strategies to help you stay driven, even on the tough days.
Understanding Motivation: Intrinsic vs. Extrinsic Motivation can come from two main sources: intrinsic and extrinsic. Intrinsic motivation is when you are driven by internal factors—like the feeling of accomplishment after a great workout or the desire to improve your health. On the other hand, extrinsic motivation comes from external factors, like rewards, praise, or comparison to others.
While extrinsic motivation can give you a quick boost, it’s intrinsic motivation that has staying power. By finding deeper, personal reasons for working out—whether it’s to feel stronger, reduce stress, or improve your quality of life—you can cultivate a more lasting drive to push yourself.
Setting Clear, Achievable Goals One of the most powerful ways to stay motivated is by setting clear and achievable goals. The key to goal-setting is to break your bigger, long-term goals into smaller, actionable steps. For example, if your goal is to lose 20 pounds, set smaller milestones like losing 1-2 pounds each month. This makes the goal feel more attainable and prevents overwhelm.
Write your goals down and keep them visible. This serves as a constant reminder of why you’re putting in the work. You can also use goal-tracking apps or journals to track your progress. Celebrate each milestone along the way to maintain momentum and keep your motivation high.
Building Habits Through Consistency Once you’ve set your goals, it’s time to turn them into habits. Habits are powerful because they are automatic. When you work out regularly, it becomes a non-negotiable part of your routine, like brushing your teeth. The key to building habits is consistency. Start with small, manageable workouts and gradually increase their intensity and duration. When exercise becomes part of your daily life, motivation becomes less of a factor—it’s just something you do.
But consistency doesn’t mean perfection. On days when you’re feeling low, remind yourself that even a 15-minute workout is better than nothing. Sometimes, just showing up is the hardest part. Once you’re there, you’ll often find the motivation to push through.
Accountability and Support Accountability can be a game-changer when it comes to staying motivated. If you have someone who’s counting on you to show up, you’re more likely to follow through. Find a workout buddy who shares similar goals, or join a fitness class where you can interact with others. Social support helps keep you accountable and makes the experience more enjoyable.
With the rise of fitness apps and social media communities, there are endless opportunities to connect with others who are on a similar fitness journey. Share your progress on Instagram or in a fitness group to receive encouragement and support. Sometimes, seeing someone else’s success can reignite your own motivation.
Visualizing Success Visualizing your success can be an incredibly powerful tool. Take a few minutes each day to close your eyes and imagine how great it will feel when you’ve reached your fitness goals. Picture yourself feeling stronger, more confident, and healthier. Visualizing success helps keep you focused and reminds you of the rewards that await at the end of your journey.
Embracing Setbacks No one’s fitness journey is perfect. There will be setbacks—whether it’s an injury, a busy week, or simply losing motivation for a while. Instead of seeing these setbacks as failures, view them as part of the process. Everyone experiences bumps in the road, but it’s how you respond to them that matters.
When you’re facing a setback, take a step back and evaluate what’s going on. Maybe you need more rest, or perhaps your goals need adjusting. Setbacks offer valuable learning opportunities. Use them to reassess and refocus, not as a reason to give up.
Creating a Reward System Sometimes, motivation needs a little extra push, and rewarding yourself is a great way to keep things fun. Set up a reward system where you treat yourself when you reach milestones. This could be something small like a new workout outfit after hitting a fitness goal, or a relaxing day at the spa after completing a challenging workout plan. Rewards act as positive reinforcement, helping you stay excited about your fitness journey.
Key Takeaways:
Intrinsic motivation is more sustainable than extrinsic motivation.
Set clear, realistic goals and break them down into manageable steps.
Consistency turns workouts into habits, reducing the reliance on motivation',
    '3'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'The Science Behind Weight Loss: What You Need to Know',
    '4',
    'images/blog_img/blog4.jpg',
    'Understanding the science behind weight loss can help you make informed decisions about your fitness journey. This blog explores how weight loss works and how to approach it effectively.',
    'Weight loss is a topic that’s often oversimplified. There are countless diets, fads, and quick fixes claiming to offer miraculous results. However, the science behind weight loss is much more complex and involves a deeper understanding of how the body burns fat and processes food. In this blog, we’ll explore the key principles of weight loss and how you can approach it in a healthy, sustainable way.
The Role of Calories and Energy Balance At its core, weight loss is governed by the principle of energy balance. This means that in order to lose weight, you need to burn more calories than you consume. This is known as a calorie deficit. Your body requires a certain number of calories to maintain basic functions like breathing, digestion, and even sleeping. These are called your basal metabolic rate (BMR).
When you eat more calories than your body needs, the excess is stored as fat. To lose fat, you must create a calorie deficit by either reducing your calorie intake, increasing your physical activity, or both. However, creating too large of a calorie deficit can lead to muscle loss, nutrient deficiencies, and metabolic slowdown. Therefore, it’s important to aim for a moderate calorie deficit, typically 500-750 calories per day, which results in a safe and sustainable weight loss of 1-2 pounds per week.
The Importance of Nutrition While calorie balance is critical, the quality of the calories you consume is just as important. A diet high in processed foods, sugars, and unhealthy fats can lead to weight gain, regardless of your calorie intake. On the other hand, a nutrient-dense diet filled with whole foods—lean proteins, vegetables, whole grains, and healthy fats—can promote fat loss and improve overall health.
Protein is particularly important when losing weight. It helps preserve lean muscle mass while you’re in a calorie deficit, preventing your metabolism from slowing down too much. Additionally, protein promotes satiety, meaning you feel fuller for longer, which can help you stick to a reduced-calorie diet.
Exercise and Its Role in Weight Loss Exercise is another crucial component of weight loss. While diet plays a larger role in creating a calorie deficit, exercise accelerates the process and helps prevent muscle loss. Cardiovascular exercise, such as running, cycling, or swimming, helps you burn calories and improve cardiovascular health. Strength training is also essential, as it helps build lean muscle, which in turn boosts your metabolism.
A combination of both cardio and strength training is the most effective approach to weight loss. Aim to engage in strength training 2-3 times per week and incorporate cardio into your routine 3-5 days per week.
Metabolism and Weight Loss Your metabolism is the process by which your body converts food into energy. People with faster metabolisms tend to burn more calories at rest, making weight loss easier for them. While metabolism is largely determined by genetics, you can give it a boost by increasing your muscle mass, staying active, and eating enough protein.
Mindset and Patience Finally, weight loss requires patience and consistency. There will be days when the scale doesn’t move, and that’s okay. It’s essential to focus on the bigger picture, which includes how you feel, your energy levels, and other non-scale victories like improved strength or endurance.
Weight loss is a marathon, not a sprint. Stay consistent with your workouts, focus on whole foods, and trust the process. Over time, the results will follow.
Key Takeaways:
Weight loss is achieved through a calorie deficit—burning more calories than you consume.
A balanced diet of whole foods and adequate protein is essential.
Combine cardio and strength training for optimal fat loss and muscle preservation.
Patience and consistency are key—trust the process and focus on the journey.',
    '4'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Fitness for Beginners: How to Start Your Fitness Journey on the Right Foot',
    '1',
    'images/blog_img/blog5.jpg',
    'Starting your fitness journey can feel overwhelming, but with the right approach, anyone can succeed. This blog provides a beginner-friendly guide to kickstart your fitness routine and stay on track for long-term success.',
    'Starting a fitness journey can be daunting. Whether you’ve never exercised before or have been inactive for a while, the thought of getting started can feel intimidating. But the truth is, everyone has to start somewhere. The key to success is breaking down the process into manageable steps, setting realistic expectations, and building confidence along the way. In this blog, we’ll guide you through the best practices for beginners to ensure you set off on the right foot.
Start Slow and Build Up Gradually One of the biggest mistakes beginners make is jumping into a rigorous routine too quickly. While enthusiasm is great, overexerting yourself early on can lead to burnout, injury, or discouragement. Instead, begin with short and manageable workouts that focus on building a foundation.
Start with exercises that target your major muscle groups, such as squats, lunges, push-ups, and planks. Begin with lighter weights or bodyweight exercises and focus on mastering your form before increasing the intensity or weight. As your body adapts, you can gradually increase the difficulty of your workouts.
If you’re new to cardio, start with low-impact exercises like walking, cycling, or swimming. As your endurance improves, you can incorporate more intense activities like running or interval training. Remember, the goal in the beginning is consistency, not intensity.
Set Realistic Goals One of the most powerful ways to stay motivated as a beginner is by setting realistic and achievable goals. These goals can be both short-term and long-term, but they should be specific and measurable.
For example, a short-term goal could be something like "I will exercise for 30 minutes, three times a week." A long-term goal could be "I want to lose 10 pounds in three months" or "I want to be able to do 10 push-ups by the end of the month."
Setting these small goals allows you to celebrate milestones along the way and helps you stay focused on progress, not perfection. Tracking your progress, whether through a fitness app or a journal, can provide a sense of accomplishment and motivate you to keep going.
Focus on Form Over Speed or Weight One of the most important principles in fitness, especially as a beginner, is focusing on form. Whether you’re lifting weights, doing bodyweight exercises, or performing cardio, using proper form ensures you’re getting the maximum benefit from your workout while reducing the risk of injury.
If you’re unsure about your form, consider working with a personal trainer, even for a few sessions. They can help you learn the correct posture and movement patterns for each exercise. Many gyms also offer free form checks or classes that are beginner-friendly, so don’t be afraid to ask for help.
Make It Fun and Enjoyable Fitness shouldn’t feel like a punishment—it should be something you enjoy. If you don’t like running, don’t force yourself to run. Instead, try other activities that interest you, like dancing, cycling, or group fitness classes. The more fun you have, the more likely you are to stick with it.
Explore different types of workouts to find what excites you. Maybe you enjoy yoga for flexibility and relaxation, or perhaps weight training to build strength. You might even try a variety of activities to keep your routine fresh and exciting. When you find what you love, fitness will feel less like a chore and more like a rewarding part of your lifestyle.
Stay Consistent and Patient As a beginner, it’s easy to expect rapid results. However, remember that real progress takes time. Be patient with yourself and focus on consistency rather than perfection. Even on days when motivation feels low, try to maintain your commitment to your routine. Even a light workout is better than no workout at all.
Over time, you’ll start noticing improvements, whether it’s in your strength, endurance, flexibility, or mood. Celebrate these small wins, and remember that fitness is a marathon, not a sprint.
Nutrition and Recovery Proper nutrition and recovery are just as important as your workouts, especially as a beginner. Your body needs the right fuel to perform at its best, so make sure you’re eating a balanced diet that includes protein, healthy fats, and complex carbohydrates. Hydration is key, so don’t forget to drink water before, during, and after your workouts.
Rest is equally important. Allow your body to recover with sufficient sleep and days off from intense training. Overworking yourself can lead to burnout and injury, so listen to your body and give it the rest it needs.
Key Takeaways:
Start slow and gradually build up intensity and duration.
Set realistic and specific goals that you can track.
Focus on form and safety, especially in the beginning.
Find activities that are fun and enjoyable to stay consistent.
Patience and consistency are essential—res',
    '5'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'The Importance of Recovery and Injury Prevention in Your Fitness Routine',
    '2',
    'images/blog_img/blog6.jpg',
    'Recovery is just as important as your workouts. Learn the best practices for recovery and injury prevention to keep your body healthy and performing at its best.',
    'When it comes to fitness, most people focus on the workouts themselves—how hard, how long, and how much they can push their bodies. But one crucial aspect of any successful fitness journey is often overlooked: recovery. Recovery is just as important as the workout itself and is essential for muscle repair, injury prevention, and overall performance improvement.
Why Recovery Matters When you exercise, you create tiny tears in your muscle fibers. These tears need time to repair and rebuild stronger than before. This process of muscle recovery happens during rest periods, not while you’re actively working out. Inadequate recovery can lead to overuse injuries, muscle imbalances, and stalled progress. If you don’t allow your muscles to recover properly, you risk overtraining, which can result in fatigue, decreased performance, and even burnout.
Types of Recovery There are several types of recovery that contribute to your overall fitness progress. Active recovery involves low-intensity exercises that allow your muscles to move without putting too much strain on them. This could be walking, cycling, or swimming at a relaxed pace. Active recovery helps maintain blood flow to the muscles, aiding in the removal of waste products and delivering nutrients for muscle repair.
Passive recovery is simply taking a rest day from exercise. This doesn’t mean you should stay completely inactive, but instead engage in activities like stretching, yoga, or foam rolling to promote blood flow to your muscles.
The Role of Sleep Sleep is one of the most powerful recovery tools your body has. During deep sleep, your body produces growth hormones that help repair and build muscle tissue. Without enough sleep, your recovery is compromised, and your performance will decline. Aim for 7-9 hours of sleep each night to ensure your body has the opportunity to recover fully.
Nutrition and Hydration for Recovery Your body needs proper nutrition to recover after a workout. Protein is essential for muscle repair, while carbohydrates help replenish glycogen stores in your muscles. Healthy fats, such as omega-3 fatty acids, play a role in reducing inflammation and promoting overall recovery.
Post-workout nutrition is crucial. Within 30 minutes of finishing your workout, aim to consume a combination of protein and carbs. A protein shake with a banana or a turkey sandwich on whole-grain bread are great examples.
Hydration also plays a key role in recovery. Water helps transport nutrients to your muscles and removes waste products, so be sure to drink plenty of water throughout the day. If you’ve had an intense workout, consider adding electrolytes to your water to replenish lost minerals.
Preventing Injuries Injury prevention should be a top priority in any fitness program. Overuse injuries, like sprains, strains, and stress fractures, can derail your progress if you’re not careful. To prevent these injuries, it’s important to listen to your body and avoid pushing too hard too quickly.
Warm-up before every workout, and incorporate dynamic stretches to prepare your muscles for exercise. After your workout, cool down with static stretches to increase flexibility and reduce muscle tension. Foam rolling can also help reduce tightness and improve mobility, which can prevent injuries in the future.
Strengthening Weak Areas A balanced workout routine is essential for injury prevention. Focus on all muscle groups, and dont neglect any area of your body. Strengthening weak areas, such as your core or stabilizing muscles, can improve your overall posture and reduce the risk of injury during more intense exercises.
Key Takeaways:
Recovery is essential for muscle repair and injury prevention.
Incorporate both active and passive recovery techniques.
Sleep, nutrition, and hydration play vital roles in recovery.
Prevent injuries by warming up, cooling down, and listening to your body.
Strengthen weak areas and maintain a balanced workout routine.',
    '6'
);


INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Fueling Your Body: The Ultimate Nutrition Guide for Fitness Enthusiasts',
    '3',
    'images/blog_img/blog7.jpg',
    'Proper nutrition is a key pillar of fitness success. This blog dives deep into the foods and strategies that will help you fuel your body for maximum performance, muscle growth, and recovery.',
    'When it comes to fitness, we often focus on the intensity of our workouts and overlook an equally important factor: nutrition. The food you eat plays a pivotal role in your overall performance, muscle growth, fat loss, and recovery. Understanding how to fuel your body with the right nutrients will ensure that your hard work in the gym yields the best possible results.
Why Nutrition Matters The relationship between exercise and nutrition is a two-way street. On one hand, physical activity requires energy, which comes from the foods you eat. On the other hand, your diet provides the nutrients necessary to repair and build muscle tissue after intense workouts. Simply put, if you’re not fueling your body properly, your fitness results will be limited.
Proper nutrition helps maintain energy levels, supports recovery, enhances muscle growth, and even improves mental clarity and focus. If you want to achieve your fitness goals, fueling your body correctly should be a top priority.
Macronutrients: The Big Three To optimize your nutrition for fitness, it’s important to understand the role of macronutrients: carbohydrates, protein, and fats. These three nutrients are the building blocks of a balanced diet and play specific roles in your fitness journey.
Carbohydrates: Carbs are your body’s primary source of energy. They’re especially important before and after workouts, as they replenish glycogen stores and give you the fuel to perform at your best. Opt for complex carbohydrates like whole grains, vegetables, and fruits, which provide sustained energy. Avoid refined sugars and processed carbs, as they cause energy crashes.
Protein: Protein is the cornerstone of muscle repair and growth. After a workout, your muscles experience tiny tears that need to be repaired. Protein helps rebuild these muscles stronger. Aim to consume a source of lean protein with each meal, such as chicken, turkey, fish, tofu, or legumes. Protein is also essential for satiety, helping you feel fuller longer and preventing overeating.
Fats: Healthy fats are crucial for hormone regulation and joint health. They also provide a steady source of energy, particularly during longer or more intense workouts. Include sources of healthy fats in your diet, such as avocados, olive oil, nuts, and seeds. Omega-3 fatty acids, found in fatty fish and flaxseeds, can help reduce inflammation and improve recovery.
Micronutrients: Vitamins and Minerals While macronutrients are the stars of the nutrition show, micronutrients—vitamins and minerals—are just as important for overall health and performance. These nutrients help with everything from immune function to muscle contraction and recovery.
Vitamin D is essential for bone health and muscle function. Spending time in the sun and eating vitamin D-rich foods like fatty fish, eggs, and fortified dairy products can help keep your levels up.
Magnesium is another important mineral that supports muscle function and reduces muscle cramps. Sources of magnesium include leafy greens, almonds, bananas, and dark chocolate.
Iron is vital for transporting oxygen to muscles during exercise. Ensure you’re getting enough iron from sources like red meat, spinach, lentils, and beans.
Don’t forget to drink plenty of water to stay hydrated—especially during and after workouts. Dehydration can impair performance and hinder muscle recovery, so aim to drink water consistently throughout the day.
Meal Timing for Optimal Performance When you eat is just as important as what you eat. Timing your meals around your workouts can have a big impact on performance and recovery.
Pre-Workout: Eat a balanced meal 1-2 hours before exercise. This should include complex carbs for energy, protein for muscle support, and a small amount of healthy fat. For example, oatmeal with almond butter and a banana or a turkey sandwich on whole-grain bread.
Post-Workout: After your workout, your muscles need nutrients to repair and grow. Aim to consume a meal or snack with both protein and carbohydrates within 30-60 minutes after exercise. This replenishes glycogen stores and supports muscle repair. A protein shake with a piece of fruit or a chicken and quinoa bowl are great options.
The Role of Supplements While food should be your primary source of nutrition, certain supplements can help fill any gaps in your diet. Popular supplements for fitness enthusiasts include:
Protein powder: If you’re not getting enough protein through whole foods, protein powder can be an easy way to meet your needs.
',
    '2'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Fitness Challenges: Push Your Limits and Stay Motivated',
    '4',
    'images/blog_img/blog8.jpg',
    'Fitness challenges can be a fun and motivating way to level up your workouts. Learn how to create or participate in fitness challenges to push your limits and stay motivated.',
    'Fitness challenges are an excellent way to add excitement, variety, and a sense of purpose to your fitness routine. Whether you’re aiming to break personal records, build strength, or simply stay motivated, fitness challenges offer an opportunity to push your limits and test your commitment to your fitness goals. In this blog, we’ll explore the benefits of fitness challenges and how to incorporate them into your routine.
Why Participate in Fitness Challenges? Participating in fitness challenges can be incredibly motivating, especially when you’re feeling stuck in a workout rut. These challenges often push you outside your comfort zone and force you to aim higher, which can reignite your passion for fitness.
There are numerous reasons why fitness challenges are beneficial:
Accountability: A challenge holds you accountable, whether you’re doing it alone or with a group. Committing to a challenge makes you more likely to follow through on your workouts, knowing there’s a defined end goal.
Variety: Challenges often introduce new exercises, movements, or training methods. This variety can break up the monotony of your usual routine and keep things interesting.
Progress Tracking: Fitness challenges typically involve measurable goals, such as running a specific distance, completing a certain number of reps, or lifting a specific weight. This allows you to track your progress and see improvements over time.
Sense of Accomplishment: Completing a fitness challenge, no matter how big or small, gives you a huge sense of accomplishment. The pride of reaching your goal can boost your confidence and provide a sense of purpose in your fitness journey.
Types of Fitness Challenges There are many types of fitness challenges, and you can customize them to fit your specific goals. Here are a few examples:
Strength Challenges: These could involve lifting a certain weight, achieving a certain number of reps, or completing an endurance test like a plank hold or push-up challenge.
Cardio Challenges: Running a certain distance, completing a series of sprints, or achieving a set number of steps per day are all great examples of cardio challenges that can help improve cardiovascular endurance.
Flexibility and Mobility Challenges: These challenges focus on increasing your range of motion and flexibility. You might challenge yourself to do a daily stretch routine or improve your yoga poses over time.
Mindset and Consistency Challenges: Sometimes, the hardest part of fitness is showing up every day. Challenges that require you to exercise for a set number of days in a row or complete a daily habit can help strengthen your mental toughness and build consistency.
How to Start Your Own Fitness Challenge Starting your own fitness challenge is easy, and it can be tailored to your personal goals and fitness level. Here’s how:
Set a Clear Goal: Your challenge should have a clear and measurable goal. It could be something like "Complete 50 push-ups in a row" or "Run 100 miles in a month."
Make It Achievable: Set a goal that challenges you but is still achievable. If your goal is too difficult, it can lead to frustration. On the other hand, a goal that’s too easy won’t provide the motivation you need to push yourself.
Track Your Progress: Use a fitness tracker or journal to monitor your progress throughout the challenge. Tracking allows you to see improvements and stay on track.
Invite a Friend or Group: Doing a challenge with a friend or group adds an element of fun and accountability. You can motivate each other and celebrate your successes together.
Celebrate Your Achievement: Once you’ve completed the challenge, take time to celebrate your achievement! Whether it’s a small reward, like treating yourself to a new workout gear or simply taking pride in your accomplishment, celebrating keeps you motivated for future challenges.
Key Takeaways:
Fitness challenges add variety, motivation, and a sense of accountability to your routine.
They help you track progress and build mental toughness.
Customize challenges to fit your personal fitness goals and level.
Invite a friend',
    '8'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Couch to 5K: How to Go from Couch Potato to Running 5K',
    '1',
    'images/blog_img/blog9.jpg',
    ' If youve ever dreamed of running a 5K but don’t know where to start, the Couch to 5K program is the perfect way to ease into running. This blog walks you through the Couch to 5K program, offering tips and motivation for those ready to go from the couch to the finish line.',
    'The idea of running a 5K can seem like an impossible goal, especially if you’ve never run before. But the Couch to 5K (C25K) program has helped thousands of people just like you go from being sedentary to crossing the finish line of their first race. It’s a gradual, structured approach designed to ease you into running, helping you build endurance without the risk of injury or burnout.
What is Couch to 5K? Couch to 5K is a popular running program designed to get you running 3.1 miles (5 kilometers) in just nine weeks. It’s perfect for beginners or people who have never run before, as it starts with a combination of walking and jogging and gradually increases your running intervals.
The idea is to build up your stamina slowly and steadily. Youll run three times a week, with rest days in between to allow your body to recover. The program progresses at a pace that helps prevent injury while allowing your body to adapt to running.
The Basic Structure of the Program The Couch to 5K program typically lasts 9 weeks, with each week’s training plan getting progressively more challenging. Here’s an example of what your first few weeks might look like:
Week 1: Alternate 60 seconds of running with 90 seconds of walking, for a total of 20 minutes.
Week 2: Alternate 90 seconds of running with 2 minutes of walking, for a total of 20 minutes.
Week 3: Alternate 2 minutes of running with 1.5 minutes of walking, for a total of 25 minutes.
As you progress, the amount of time spent running increases, and walking intervals decrease.
Each week builds on the previous one, helping you develop the stamina to eventually run for 30 minutes without stopping.
Tips for Success:
Be Consistent: Stick to the schedule and aim for three workouts per week. Consistency is key to building endurance and seeing results.
Rest and Recover: Don’t skip your rest days. Your muscles need time to recover and rebuild, which will help you avoid injury.
Listen to Your Body: If you feel pain (other than typical muscle soreness), take a step back. You can repeat a week if necessary or take extra rest days to prevent injury.
Celebrate Milestones: Each time you complete a week, celebrate your progress! The sense of accomplishment after completing each workout will keep you motivated and focused on your goal.
Stay Hydrated and Fuel Your Body: Proper hydration and nutrition will give you the energy you need to power through your runs. Eat a small snack before running, and refuel with protein and carbs afterward.
Benefits of Couch to 5K: The Couch to 5K program offers several benefits:
Improved Cardiovascular Health: Running increases heart health, improves lung capacity, and lowers the risk of heart disease.
Weight Loss: Running is an excellent fat-burning exercise, helping you lose weight and improve body composition.
Mental Health Benefits: Regular exercise like running helps reduce stress, anxiety, and depression, while boosting your mood and mental clarity.
Sense of Accomplishment: Completing your first 5K gives you a sense of pride and achievement, which can improve your self-esteem and motivate you to continue your fitness journey.
Key Takeaways:
The Couch to 5K program is an excellent way for beginners to start running and prepare for a 5K race.
Consistency, recovery, and listening to your body are important for success.
Celebrate your progress, and don’t be afraid to take it one step at a time.',
    '5'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'The Truth About Weight Loss: Sustainable Strategies for Lasting Results',
    '2',
    'images/blog_img/blog10.jpg',
    'Losing weight can be overwhelming with all the conflicting advice out there. This blog provides realistic and sustainable strategies for weight loss that focus on a balanced lifestyle rather than quick fixes or fad diets.',
    'When it comes to weight loss, there’s no shortage of trendy diets, quick fixes, and misleading advice. But the truth is, sustainable weight loss is not about restrictive diets or extreme workouts. It’s about creating healthy habits that you can maintain in the long term.
If you’re tired of bouncing from one fad diet to the next, this blog is for you. We’re going to break down the truth about weight loss and provide strategies that actually work for long-term success.
1. Start with a Balanced Diet One of the biggest myths about weight loss is that you need to deprive yourself of all the foods you love. While calorie restriction is necessary to lose weight, this doesn’t mean you have to cut out entire food groups. A balanced, whole-food-based diet will provide the nutrients your body needs while keeping you satisfied.
Focus on Whole Foods: Eat a variety of vegetables, fruits, whole grains, lean proteins, and healthy fats. These nutrient-dense foods will keep you full longer and provide the energy needed for workouts and daily activities.
Portion Control is Key: Even healthy foods can contribute to weight gain if you overeat them. Learning to control portion sizes is one of the most important factors in weight loss.
2. Consistency Over Perfection Rather than obsessing over perfect eating habits, focus on being consistent. Don’t expect to be perfect every day—what matters most is sticking to healthy habits over time. One day of indulgence won’t ruin your progress if you get back on track the next day.
In fact, incorporating occasional indulgences into your diet can help prevent feelings of deprivation and keep you from binge eating. The goal is balance, not perfection.
3. Increase Physical Activity Exercise is another critical component of weight loss. Aim to include a combination of cardio, strength training, and flexibility exercises in your routine. Exercise burns calories and helps preserve muscle mass while you lose weight. Strength training, in particular, helps boost your metabolism and build lean muscle, which burns more calories at rest.
Find Activities You Enjoy: The best way to stay active is to find exercises you enjoy. Whether it’s running, dancing, swimming, or weightlifting, doing something you love will keep you motivated.
4. Mindful Eating Mindful eating is about paying attention to how, when, and why you eat. It’s easy to fall into the trap of eating out of stress, boredom, or habit. By being more mindful, you can become more aware of your body’s hunger and fullness cues and avoid overeating.
Practice eating without distractions (like your phone or TV) and focus on enjoying your food. Slowing down and savoring each bite can also help prevent overeating.
5. Get Enough Sleep and Manage Stress Sleep and stress are often overlooked in the weight loss equation, but they play a significant role in your ability to lose weight. Poor sleep can increase hunger hormones and lead to overeating, while chronic stress can cause the body to store fat, especially around the belly.
Aim for 7-9 hours of sleep each night and find effective ways to manage stress, such as through yoga, meditation, or deep breathing exercises.
Key Takeaways:
Sustainable weight loss is about consistency and balance, not perfection or extreme diets.
Focus on whole, nutrient-dense foods and practice portion control.
Exercise, sleep, and stress management are crucial components of weight loss.
Mindful eating can help you avoid overeating and improve your relationship with food',
    '4'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Developing a Champion Mindset: How to Stay Motivated Even When You Feel Like Quitting',
    '1',
    'images/blog_img/blog11.jpg',
    ' Motivation can be fleeting, but developing a champion mindset can help you push through difficult times. This blog explains how to stay motivated and focused on your fitness goals, even when obstacles arise.',
    'When you first begin a fitness journey, it’s easy to be motivated. You’re excited, full of energy, and ready to hit the gym. But over time, that initial excitement fades, and you start facing the inevitable struggles—whether it’s a lack of time, feeling tired, or simply not seeing results as quickly as you’d like. This is when developing a champion mindset becomes essential.
What is a Champion Mindset? A champion mindset is all about resilience, focus, and mental strength. It’s the ability to stay committed to your goals even when things get tough. Whether you’re facing self-doubt, setbacks, or fatigue, a champion mindset helps you overcome obstacles and continue moving forward.
1. Set Clear, Realistic Goals One of the first steps in cultivating a champion mindset is setting clear and realistic goals. Without a clear target, it’s easy to lose direction. Define what success looks like to you, and break down your larger goals into smaller, manageable steps. Celebrate small victories along the way to stay motivated.
2. Embrace the Struggle The road to success is rarely smooth. There will be days when you feel like giving up, and that’s okay. Instead of avoiding challenges, embrace them. Every struggle is an opportunity to learn, grow, and become mentally stronger. Remember, growth happens outside your comfort zone.
3. Focus on the Process, Not Just the Outcome It’s easy to get discouraged when you’re focused solely on the outcome. Instead, shift your focus to the process itself. Enjoy the journey and celebrate the small improvements you make each day. This helps prevent frustration and keeps you motivated in the long run.
4. Stay Positive and Reframe Negative Thoughts A positive mindset can make all the difference in staying motivated. When negative thoughts creep in, such as “I’m too tired” or “I’m not making progress,” reframe them into positive affirmations like, “I am strong” or “Every step forward counts.” This mental shift can keep you on track and motivated.
5. Surround Yourself with Support A champion doesn’t go at it alone. Surround yourself with a supportive network of friends, family, or a workout buddy who can cheer you on during difficult times. Having people to encourage and hold you accountable can make the journey much more enjoyable.
Key Takeaways:
A champion mindset is about resilience, focus, and overcoming challenges.
Set clear, realistic goals and celebrate small victories along the way.
Embrace struggles as opportunities for growth and focus on the process, not just the outcome.
Reframe negative thoughts and surround yourself with supportive people to stay motivated.',
    '3'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'Mastering Motivation: How to Stay Committed to Your Fitness Goals',
    '4',
    'images/blog_img/blog12.jpg',
    'Staying motivated can be challenging, especially when you’re not seeing immediate results. In this blog, we explore strategies for staying committed to your fitness goals and maintaining motivation over time.',
    'We’ve all been there—feeling highly motivated at the start of a fitness journey, but struggling to stay on track as time goes on. The key to long-term success isn’t just about having motivation at the start, but finding ways to stay committed when motivation wanes.
1. Define Your "Why" One of the most powerful ways to stay motivated is to connect with your deeper "why." Why do you want to get fit? Is it for better health, more energy, to look and feel your best, or something else? When you connect with your deeper motivation, you create a stronger emotional attachment to your goals, making it easier to stay committed.
2. Make Fitness a Habit Motivation is often fleeting, but habits stick. By making fitness a regular part of your routine, it becomes something you do automatically rather than something you have to force yourself to do. Schedule your workouts just like any other important task, and treat them as non-negotiable.
3. Break Down Big Goals into Smaller Steps Big goals can feel overwhelming, especially if progress is slow. Break down your larger goals into smaller, more manageable steps. This helps prevent burnout and keeps you focused on achieving one small victory at a time.
4. Track Your Progress Seeing progress is one of the best ways to stay motivated. Whether its tracking your weight, measurements, or fitness levels, tracking your progress helps you visualize your success. Even small improvements are worth celebrating and can keep you going.
5. Find Your Fitness Tribe Fitness doesn’t have to be a solo journey. Finding a group of like-minded individuals can provide accountability and motivation. Whether its a fitness class, an online community, or a workout buddy, having a support system will make sticking to your fitness goals much easier.
Key Takeaways:
Connect with your deeper "why" to find lasting motivation.
Make fitness a habit by scheduling regular workouts.
Break down big goals into smaller, achievable steps.
Track progress and celebrate small victories to stay motivated.
Surround yourself with a supportive fitness community to keep you accountable.',
    '3'
);

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    '10 Simple Habits to Boost Your Health & Wellbeing Every Day',
    '3',
    'images/blog_img/blog13.jpg',
    'Small daily habits can lead to massive improvements in your overall health and wellbeing. In this blog, we explore 10 simple, sustainable habits that can help you feel your best physically and mentally.',
    'Taking care of your health and wellbeing doesn’t have to be overwhelming. In fact, the smallest changes to your daily routine can make the biggest impact over time. In this blog, we’re diving into 10 simple habits that you can incorporate into your everyday life to boost both your physical and mental health.
1. Start Your Day with Hydration It’s easy to forget, but hydration is key to good health. After a night of sleep, your body is in need of water to kickstart its processes. Drinking a glass of water first thing in the morning helps to rehydrate your body, boosts energy levels, and supports digestion. Try adding a slice of lemon to your water for extra detox benefits.
2. Move Your Body Daily You don’t need to run a marathon every day, but incorporating movement into your day is essential for maintaining good health. Whether it’s a brisk walk, yoga, or a quick workout session, daily movement keeps your body strong, helps to relieve stress, and boosts your mood through the release of endorphins.
3. Practice Mindfulness or Meditation Mindfulness or meditation doesn’t have to take hours of your day. Just 5-10 minutes of deep breathing, guided meditation, or a mindful walk can significantly reduce stress and improve mental clarity. A calm mind supports better decision-making, improves focus, and helps with emotional balance.
4. Prioritize Sleep Sleep is one of the most important aspects of health that people often overlook. Getting enough rest is essential for your body’s repair processes, boosting immune function, and improving cognitive function. Aim for 7-9 hours of quality sleep each night. If you struggle with sleep, try developing a relaxing bedtime routine, limiting screen time before bed, and keeping your room cool and dark.
5. Eat More Whole Foods The foundation of a healthy diet starts with whole, unprocessed foods. Focus on fruits, vegetables, whole grains, lean proteins, and healthy fats. These nutrient-dense foods provide your body with the energy and nutrients it needs to function at its best. Remember, healthy eating is about balance, not restriction.
6. Get Outdoors Spending time outdoors has numerous benefits for both physical and mental health. Nature can help reduce stress, boost mood, and improve focus. Whether you go for a hike, take a walk in the park, or simply sit outside and enjoy the fresh air, make it a point to get outside every day.
7. Practice Gratitude Starting or ending your day with gratitude can significantly improve your overall wellbeing. Take a moment to reflect on what you’re thankful for. This simple practice shifts your focus from what you don’t have to what you do, creating a sense of abundance and positivity in your life.
8. Stay Connected to Loved Ones Human connection is essential for emotional health. Make time to reach out to family and friends, whether it’s through a phone call, a text, or in person. Positive relationships foster a sense of belonging, reduce stress, and improve your mood.
9. Limit Screen Time Excessive screen time, especially before bed, can disrupt your sleep patterns and contribute to mental fatigue. Try to limit screen time, particularly social media, to avoid information overload and emotional drain. Consider implementing a "digital detox" where you unplug from screens for an hour or two each day to reconnect with yourself and the world around you.
10. Practice Deep Breathing Deep breathing exercises can have a profound impact on your stress levels, mood, and overall wellbeing. Whenever you feel stressed, anxious, or overwhelmed, take a moment to pause, breathe deeply, and center yourself. Deep breathing helps activate your parasympathetic nervous system, calming your body and mind.
Key Takeaways:
Small daily habits can lead to significant improvements in your physical and mental health.
Hydration, movement, mindfulness, sleep, and whole foods are key to a healthier lifestyle.
Building a routine around simple, sustainable habits can help you feel your best every day.',
    '7'
    );

INSERT INTO blog (title, author_id, image, summary, content, category_id)
VALUES (
    'How to Build a Healthy Mind-Body Connection for Total Wellbeing',
    '1',
    'images/blog_img/blog14.jpg',
    'Your mind and body are deeply connected, and nurturing this connection is essential for total wellbeing. This blog dives into how you can strengthen the mind-body connection to enhance both your mental and physical health.',
    'When it comes to overall wellbeing, many people focus solely on physical health or mental health, but the truth is that your mind and body are interconnected. The way you think, feel, and perceive the world directly impacts how your body functions, and vice versa. Developing a healthy mind-body connection can lead to improved mental clarity, emotional stability, and physical vitality.
In this blog, we’ll explore the importance of the mind-body connection and offer practical tips to help you nurture this bond for a healthier, more balanced life.
1. Understand the Link Between Mind and Body Your thoughts, emotions, and stress levels can affect your physical health. Chronic stress, for example, can lead to inflammation, poor digestion, and weakened immune function. On the other hand, your physical health can impact your mental wellbeing. Poor sleep, inactivity, or poor nutrition can contribute to feelings of anxiety, depression, or lack of focus.
By acknowledging and understanding this powerful connection, you’re better equipped to take care of both aspects of your health.
2. Engage in Mindful Movement Movement is an excellent way to connect with both your body and mind. Practices like yoga, tai chi, and Pilates focus on mindful movement, incorporating breathwork and awareness. These practices not only improve strength, flexibility, and balance, but they also help to cultivate a deeper connection between your mind and body.
Even if yoga or tai chi isn’t your style, any form of exercise can help enhance the mind-body connection. Activities such as walking, swimming, or dancing allow you to focus on how your body feels and moves, bringing mindfulness into your physical activity.
3. Practice Deep Breathing Techniques Breathing exercises are a simple yet powerful tool to connect your mind and body. Slow, deep breaths activate the parasympathetic nervous system, calming the body’s stress response. Breathing exercises also help to focus your mind, bringing awareness to the present moment. Techniques like diaphragmatic breathing, box breathing, or alternate nostril breathing can promote relaxation and improve mental clarity.
4. Eat Mindfully What you eat plays a significant role in how you feel mentally and physically. When you eat mindfully—without distractions like TV or smartphones—you bring awareness to the food you’re consuming. This can improve digestion, prevent overeating, and help you develop a healthier relationship with food. Focus on whole foods, and notice how different foods make you feel. Eating mindfully can create a deeper sense of satisfaction, both mentally and physically.
5. Rest and Sleep for Recovery Rest is essential for both mental and physical recovery. When you’re well-rested, you’re better able to manage stress, think clearly, and maintain emotional balance. Sleep is when your body heals and restores itself, and it’s just as important as nutrition and exercise. Make sleep a priority by developing a calming bedtime routine, limiting screen time, and creating a sleep-friendly environment.
6. Practice Gratitude for Mental and Emotional Wellbeing Gratitude is one of the most powerful practices for improving your emotional wellbeing. When you express gratitude, you shift your mindset from focusing on what’s wrong to appreciating what’s going well. This positive shift in perspective has been shown to reduce stress, improve mood, and even enhance physical health. Start or end each day by reflecting on a few things you’re grateful for, and notice how it affects your overall wellbeing.
7. Take Time for Self-Care Self-care is essential for nurturing both your mind and body. This can include anything from a relaxing bath, reading a book, or spending time in nature. Prioritize activities that bring you joy and relaxation, allowing you to recharge mentally and physically. Regular self-care helps to reduce stress, improve mood, and support your overall health.
Key Takeaways:
Nurturing the mind-body connection is crucial for total health and wellbeing.
Practices like mindful movement, deep breathing, and mindful eating can strengthen this connection.
Sleep, gratitude, and regular self-care are essential components of maintaining balance in your life.
Prioritize activities that promote both physical and mental health to achieve long-term wellbeing.',
    '7'
    );

select * from blog;


                                    -- meal plan --


CREATE TABLE meal_plans (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL,
    name VARCHAR(255),
    description TEXT,
    meals JSON,
    created_at DATETIME,
    FOREIGN KEY (member_id) REFERENCES member(member_id) on delete cascade
);

INSERT INTO meal_plans (member_id, name, description, meals, created_at)
VALUES
(1,
 'Week of 14-04-25',
 'Healthy and balanced meal plan for the week',
 '{"Monday": {"breakfast": "Oatmeal", "lunch": "Chicken Salad", "dinner": "Grilled Salmon", "snacks": "Apple"}, "Tuesday": {"breakfast": "Scrambled Eggs", "lunch": "Pasta", "dinner": "Steak", "snacks": "Nuts"}, "Wednesday": {"breakfast": "Smoothie", "lunch": "Veggie Wrap", "dinner": "Chicken Stir Fry", "snacks": "Carrot Sticks"}, "Thursday": {"breakfast": "Avocado Toast", "lunch": "Quinoa Salad", "dinner": "Grilled Chicken", "snacks": "Banana"}, "Friday": {"breakfast": "Pancakes", "lunch": "Sushi", "dinner": "Tacos", "snacks": "Yogurt"}, "Saturday": {"breakfast": "Egg Muffins", "lunch": "Salmon Wrap", "dinner": "Baked Ziti", "snacks": "Grapes"}, "Sunday": {"breakfast": "Bagels", "lunch": "Steak Salad", "dinner": "Chicken Parmesan", "snacks": "Popcorn"}}',
 '2025-04-14 14:21:33');

 INSERT INTO meal_plans (member_id, name, description, meals, created_at)
VALUES
(1,
 'Week of 07-04-25',
 'Vegan meal plan for the week',
 '{"Monday": {"breakfast": "Avocado Toast", "lunch": "Vegan Burrito", "dinner": "Lentil Stew", "snacks": "Almonds"}, "Tuesday": {"breakfast": "Smoothie Bowl", "lunch": "Chickpea Salad", "dinner": "Tofu Stir Fry", "snacks": "Hummus with Carrots"}, "Wednesday": {"breakfast": "Chia Pudding", "lunch": "Vegan Wrap", "dinner": "Quinoa with Vegetables", "snacks": "Fruit"}, "Thursday": {"breakfast": "Overnight Oats", "lunch": "Avocado Salad", "dinner": "Vegan Chili", "snacks": "Trail Mix"}, "Friday": {"breakfast": "Peanut Butter Toast", "lunch": "Vegan Sushi", "dinner": "Vegan Tacos", "snacks": "Popcorn"}, "Saturday": {"breakfast": "Banana Pancakes", "lunch": "Tofu Salad", "dinner": "Lentil Soup", "snacks": "Energy Balls"}, "Sunday": {"breakfast": "Vegan Smoothie", "lunch": "Rice and Beans", "dinner": "Veggie Pizza", "snacks": "Dark Chocolate"}}',
 '2025-04-07 08:45:00');

 INSERT INTO meal_plans (member_id, name, description, meals, created_at)
VALUES
(1,
 'Week of 21-04-25',
 'Meal plan focused on protein-rich meals for muscle growth',
 '{"Monday": {"breakfast": "Egg Scramble", "lunch": "Grilled Chicken Breast", "dinner": "Beef Stir Fry", "snacks": "Protein Bar"}, "Tuesday": {"breakfast": "Greek Yogurt", "lunch": "Turkey Wrap", "dinner": "Salmon with Veggies", "snacks": "Boiled Eggs"}, "Wednesday": {"breakfast": "Omelette", "lunch": "Chicken Caesar Salad", "dinner": "Steak and Sweet Potatoes", "snacks": "Almonds"}, "Thursday": {"breakfast": "Protein Shake", "lunch": "Tuna Salad", "dinner": "Grilled Chicken with Rice", "snacks": "Cottage Cheese"}, "Friday": {"breakfast": "Breakfast Burrito", "lunch": "Shrimp Salad", "dinner": "Pork Tenderloin", "snacks": "Peanut Butter"}, "Saturday": {"breakfast": "Egg White Omelette", "lunch": "Grilled Fish", "dinner": "Chicken and Broccoli", "snacks": "Greek Yogurt"}, "Sunday": {"breakfast": "Chia Pudding", "lunch": "Beef Tacos", "dinner": "Grilled Pork Chop", "snacks": "Protein Shake"}}',
 '2025-04-21 14:21:33');

INSERT INTO meal_plans (member_id, name, description, meals, created_at)
VALUES
(1,
 'Week of 31-03-25',
 'High-carb meal plan for energy and endurance',
 '{"Monday": {"breakfast": "Oatmeal with Banana", "lunch": "Pasta with Pesto", "dinner": "Rice with Grilled Chicken", "snacks": "Granola Bar"}, "Tuesday": {"breakfast": "Bagels with Cream Cheese", "lunch": "Quinoa and Veggie Stir Fry", "dinner": "Baked Potato with Chili", "snacks": "Apple with Peanut Butter"}, "Wednesday": {"breakfast": "Smoothie with Spinach", "lunch": "Whole Wheat Sandwich", "dinner": "Spaghetti with Marinara Sauce", "snacks": "Carrot Sticks with Hummus"}, "Thursday": {"breakfast": "Toast with Avocado", "lunch": "Couscous Salad", "dinner": "Sweet Potato and Black Bean Tacos", "snacks": "Rice Cakes"}, "Friday": {"breakfast": "French Toast", "lunch": "Vegetable Soup", "dinner": "Risotto", "snacks": "Fruit Salad"}, "Saturday": {"breakfast": "Pancakes with Maple Syrup", "lunch": "Curry Rice", "dinner": "Chicken and Rice", "snacks": "Nuts and Dried Fruit"}, "Sunday": {"breakfast": "Muesli", "lunch": "Falafel Wrap", "dinner": "Veggie Burger", "snacks": "Granola"}}',
 '2025-03-31 08:45:00');

 select * from meal_plans;