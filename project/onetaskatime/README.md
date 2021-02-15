One Task A Time 12/07/2020

General Usage Notes
***
Download all files within the project and install the Python packages required as shown in requirements.txt. Run One Task A Time under CS50 IDE by navigating to the main project folder and using Flask run in the terminal. This project took its foundation from the CS50 Finance Pset. 

Goal of One Task A Time
***
The goal of this project is to help users plan out their time by having them listing down the tasks (main goals) they'd like to work on and break these tasks down into smaller, more manageable sub-goals.

For each subgoal, they will set a time that they believe they can finish the subgoal within, and use a timer to keep track of the time they actually spend. The point of this function is to make users focus on and finish one subgoal at a time instead of multitasking (which is scientifically shown to be distracting) or worrying about the overall large project/goal. Users can also view stats showing if the time they actually spend matches up with the time they thought they would spend, which lets them analyze their working habits and accordingly plan out their day on a more accurate time schedule. Working for longer than the time they planned out also pushes users to evaluate why they might be taking longer than planned and see if they can finish tasks more efficiently or otherwise adjust their time table.

One Task A Time Usage 
***
1. Register: Register for an account. Once your account has been created, you will receive a confirmation at the top and be redirected to login to your newly created account
2. Main page: Once you login, you will be on your main page, which displays your main goals and their sub-goals in a card slideshow. With a new account, add goals to view them on the main page. If you have already added new goals, you can click the right- and left-arrow to navigate the slideshow to get to any main goal. At the bottom of the slideshow, you will see the total number of main goals you currently have and the total time planned for all of them combined.
3. You can delete main goals or subgoals on the right side of the main page. Deleting a main goal will delete all subgoals nested under that main goal (if there are any). Deleting a subgoal will delete the subgoal under the main goal where it resides. 
4. To start a task, select a subgoal from your slideshow on the main page and click “Start Timer”. You will be redirected to the countdown timer page. See #7, Timer, for more details. 
5. When you finish a main goal, you may click the “Finished Main Goal” button on the main goal, upon which the slide displaying that specific main goal, along with all of its subgoals, will disappear from the main page. 
6. Add Goals page: Add main goals in the section titled “Add Main Goals Here” and use the “Submit Goal” button directly below it. Add subgoals and their allotted time in the section entitled “Add Subgoals Here”, first choosing a main goal from the drop down menu to indicate which main goal the subgoal being entered falls under. 
7. Timer page: When redirected to the timer page after clicking “Start Timer” from the main page, the timer will start counting down from the minutes that you indicated for the time planned of the subgoal. The main goal and subgoal you are working on will be displayed at the top of the page. You may pause or restart the timer (from the paused time) using the “Pause” and “Start” buttons. To ensure maximal focus, there will be no navigation bar or links to click to navigate back/to other pages, unless you click “Stop Task”. “Stop Task” will take you back to the main page and will not delete the goal from your list. If you work for longer than the time you planned, the timer will start counting up to show you how long you have been working overtime. Spotify playlists are also embedded in the page for you to play music while working on your subgoal if you wish. When you finish the subgoal, click on “Finish Task” to be redirected back to the main page, upon which the subgoal will be deleted from your list and noted in our databases.
8. Edit Goals page: Here you can change the names and allotted times of your main goals and subgoals. To change the name of a main goal, select the main goal from the drop down menu in the top section “Edit the name of your maingoals”, type in the new name, and click submit to change. To change the name/time of a subgoal, select the subgoal from the drop down menu in the bottom section “Edit your subgoals” and type in the new name and/or time planned. You can change either just the name, just the time planned, or both at once. 
9. Change Password page: You can change your password here. Click “Change Password”, type in your old password, and then type in a new password along with the confirmation of the new password. 
10. History and Stats of completed goals page: You can select either “Past Week” or “Past Month” and view the corresponding stats summary for the goals/tasks completed by users.
11. Logging out/clocking out: To log out of the website, click “Clock Out” in the top right of the navigation bar. The website will take you to a table that shows you all of the tasks you completed during your current session as well as the time you spent doing the tasks. Click “Log Out” to fully log out of the website. 

Video URL: 
***
https://youtu.be/esmO6XvZ7hA
