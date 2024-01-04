# Pedagogical Conversational Agent Ben moderates Quiz-Game in Slack for English Learning

## Software Architecture of the Pedagogical Conversational Agent Ben
The following figure illustrates the architecture of our prototype. 
<br>
<img width="454" alt="image" src="https://github.com/tubspaulkeller/companionben/assets/102319452/7ae66caa-dc8b-4bde-a2c8-28f3ea6e240a"> 
<br>
We utilized the Rasa framework together with its software development kit (SDK) for implementation (Bocklisch et al. 2017). We use the natural language understanding pipeline to handle open-ended questions, such as inquiries about the user's score or questions related to specific verb tenses. During goal setting, the PCA provides the user with various suggestions for a learning goal. The iterative process, beginning with the initial determination of the goal and subsequent specification of the timeframe, is made possible by the use of “Rasa forms”. Moreover, the utilization of Rasa forms enables the validation of user responses to English tasks. One advantage of this validation process is the ability to integrate API calls. To verify user inputs for English tasks, we are using a language-checking tool called “LanguageTool”. This tool enables the assessment of the correctness of the response and the calculation of a score. Additionally, Rasa forms offer the opportunity for the user to respond again in the case of an incorrect answer. Before granting this opportunity, our PCA provides the user with hints through the LanguageTool API interface. With this guidance, users can independently acquire knowledge, and receive assistance by the PCA to solve the tasks. The communication channel between the user and the PCA is via the messaging tool “Slack.”

## Excerpts of the Conversations with Ben Related to the DPs

<img width="1441" alt="Screenshot 2024-01-04 at 15 35 52" src="https://github.com/tubspaulkeller/companionben/assets/102319452/3e0996f8-fbda-44ea-90d3-65830074f7ba">

Regarding DP1, learners can set SMART goals with the PCA (Doran 1981). In the beginning, Ben asks learners to formulate an overall vision for the course and provides several options to choose from, such as preparing for a semester abroad or achieving better grades. Once users select a goal, they can decide when they strive to achieve it so that the goal fits their own learning pace (Locke and Latham 1990; Latham et al. 2011). Subsequently, learners can set subgoals, such as how much vocabulary they would like to learn in the coming month to reach the overall goal. The selected overall goal and the subgoals serve as a guide for the upcoming English learning journey. The PCA then starts a quiz aligned with the learning goals, for example, practicing the new vocabulary. After completing the quiz, the PCA communicates the score in relation to the maximum number of points. Ben then reflects with the learner on the pace of learning. For example, Ben asks if the learner wants to continue at the same pace or adjust the time frame to achieve the learning goal. This feedback allows the learners to adapt their learning approach, such as the number of questions they want to tackle next, to ensure they continue to make progress. By reflecting on the progress, learners are encouraged to learn self-regulated (Scheu and Benke 2022).
In DP2, Ben acts as a more experienced classmate (Kim and Baylor 2016; Khosrawi-Rad et al. 2022b; Strohmann et al. 2022). To build trust and establish credibility, Ben states that he has already completed the exam and can thus offer helpful tips (ibid.). In the beginning, Ben provides the opportunity to get a summary of the grammatical structure relevant to the upcoming quizzes. Then, Ben first asks simple choice questions in which learners must identify which of the answers relates to a particular tense. These serve to ensure that learners internalize the scheme of the according tense. In line with Bloom's taxonomy and goal-setting theory, the difficulty of the questions increases afterward (Bloom 1956; Locke and Latham 1990; Anderson and Krathwohl 2001; Latham et al. 2011). Ben then uses open-ended questions to ask learners to form a sentence correctly using given words. We decided not to include time pressure during these tasks because research shows that it may induce cognitive stress harming students’ performance and learning experience (Ackerman and Lauterman 2012). Ben provides feedback on the correctness of the learners' written sentences and awards points based on the number of attempts to answer the question. To check the sentences for correctness, the PCA uses an API to the “LanguageTool.” If learners do not answer correctly, Ben helps the learners. The PCA can point out if the user has not used all the given words. The PCA furthermore suggests corrections if the answer contains spelling errors using the “Language Tool.” At the end of each session, Ben points out the importance of regularly reviewing the knowledge and informs the user to regularly remind him/her to repeat the tasks, similar to further English language learning literature (Pham et al. 2018; Ruan et al. 2019).
In DP3, we focus on rewarding learners’ individual performance. We decided not to implement rankings because interviewees mentioned that rankings could cause frustration, which is consistent with literature findings (Super et al. 2019). Ben rewards points based on the learner's attempts to answer the question. The learner earns five points for correctly answering on the first attempt and two points for correctly responding on the second attempt. Ben moreover grants stars to learners to recognize their accomplishments in a specific field. These stars serve as a marker of the learner's progress over a medium term.  Learners who reach long-term milestones, such as mastering two different tenses, receive a badge as a reward. Learners can level up by completing a certain number of tasks correctly. When learners reach the next level, a progress bar indicates how much of the lesson remains until completion. Overall, the positive reinforcement through different game elements aligned to short-, medium- and long-term learning goals fosters learners' perception of competency awareness (Ryan and Deci 2000; Sailer et al. 2017; Krath et al. 2021). 
In DP4, Ben helps students apply knowledge by simulating real-life situations (Forsyth et al. 2020). Therefore, Ben acts as a narrator and guides learners through a fictive case, i.e., traveling to Rome with a friend. Along the way, Ben presents learners with tasks, e.g., ordering a taxi or asking for Student tickets to the Colosseum. If learners answer incorrectly, Ben provides hints to help them correct their answers. Using quests, the story contains smaller subgoals that the learner can achieve one by one. This allows the learner feel like he/she is making progress step by step (Krath et al. 2021).

### Literature
Ackerman R, Lauterman T (2012) Taking reading comprehension exams on screen or on paper? A metacognitive analysis of learning texts under time pressure. Comput Hum Behav 28:1816–1828

Anderson LW, Krathwohl DR (2001) A taxonomy for learning, teaching, and assessing: A revision of Bloom’s taxonomy of educational objectives. Longman, New York

Bloom BS (1956) Taxonomy of educational objectives:  The classification of educational goals, 1st ed. Longman Group, Harlow, Essex,  England

Bocklisch T, Faulkner J, Pawlowski N, Nichol A (2017) Rasa: Open Source Language Understanding and Dialogue Management

Doran GT (1981) There’sa SMART way to write management’s goals and objectives. Manage Rev 70:35–36

Forsyth CM, Graesser A, Millis K (2020) Predicting Learning in a Multi-component Serious Game. Technol Knowl Learn 25:251–277

Khosrawi-Rad B, Schlimbach R, Strohmann T, Robra-Bissantz S (2022b) Design Knowledge for Virtual Learning Companions. In: AIS SIGED ICIS-ER Proc. Copenhagen, Denmark

Kim Y, Baylor AL (2016) Research-Based Design of Pedagogical Agent Roles: a Review, Progress, and Recommendations. Int J Artif Intell Educ 26:160–169

Krath J, Schürmann L, von Korflesch HFO (2021) Revealing the theoretical basis of gamification: A systematic review and analysis of theory in research on gamification, serious games and game-based learning. Comput Hum Behav 125:106963

Latham GP, Ganegoda DB, Locke EA (2011) Goal-setting: A state theory, but related to traits. In: The Wiley-Blackwell handbook of individual differences. Wiley Blackwell, Hoboken, NJ, US, pp 579–587

Locke EA, Latham GP (1990) A theory of goal setting & task performance. Prentice-Hall, Inc, Englewood Cliffs, NJ

Pham XL, Pham T, Nguyen QM, et al (2018) Chatbot as an intelligent personal assistant for mobile language learning. In: ACM International Conference Proceeding Series. pp 16–21

Ruan S, Jiang L, Xu J, et al (2019) QuizBot: A Dialogue-based Adaptive Learning System for Factual Knowledge. In: CHI Proc. 2019. New York, USA

Ryan RM, Deci EL (2000) Intrinsic and Extrinsic Motivations: Classic Definitions and New Directions. Contemp Educ Psychol 25:54–67a

Sailer M, Hense JU, Mayr SK, Mandl H (2017) How gamification motivates: An experimental study of the effects of specific game design elements on psychological need satisfaction. Comput Hum Behav 69:371–380

Strohmann T, Siemon D, Khosrawi-Rad B, Robra-Bissantz S (2022) Toward a design theory for virtual companionship. Human–Computer Interact 38:1–41

Super J, Keller RH, Betts TK, Roach Humphreys J (2019) Simulation Games: Learning Goal Orientations and Norms for Knowledge Sharing. Acad Manag Proc 2019

## Prerequisites
- Rasa
- Slack-Account 
- MongoDBAtlas
- NGROK
- LANGUAGE_TOOL_API_KEY
- DEEPL_TRANSLATOR_API_KEY

## Environments 
Create a .env file with the following variables: 
GRAMMAR_TOOL_KEY = <LANGUAGE_TOOL_API_KEY>
TRANSLATE_KEY = <DEEPL_TRANSLATOR_API_KEY>
RASA_URL = "http://localhost:5002/api"
MONGO_DB_URL = <MONGO_DB_URL>
DB_NAME = <MONGO_DB_NAME>
USERNAME = <MONGO_DB_USERNAME>
PSWD = <MONGO_DB_PASSWORD
SLACK_TOKEN_ONE = <SLACK_TOKEN>
SLACK_CHANNEL= <SLACK_CHANNEL>
SLACK_SIGNING_SECRET= <SLACK_SECRET>

## Installation 

- Install Rasa: Follow the steps at [Rasa Documentation](https://rasa.com/docs/rasa/2.x/installation/).
- Install dependent packages using: `pip install -r /Conversational-AI-Agent-For-English-Learning/requirements.txt`.
- Install NGROK from: [NGROK Download](https://ngrok.com/download).
  
### MongoDB:

Update the connection string under `/Conversational-AI-Agent-For-English-Learning/.env` for the variable `MONGO_DB_URL`.

### NGROK:

For HTTPS connection between Telegram and Rasa, use NGROK.
1. Open a terminal.
2. Run: `ngrok http 5005`.
Under Forwarding, note the URL ending with ngrok-free.app for further steps.

### RASA:
Next, open two additional terminal windows. Activate the Rasa environment in both terminals from installation. After that, in both terminals, navigate to the directory containing the source code: `/Conversational-AI-Agent-For-English-Learning/`.

1. If no model exists, run the following command in one terminal: 
    ```bash
    rasa train --domain domains 
    ```

2. Next, insert the NGROK URL into the file `/Conversational-AI-Agent-For-English-Learning/credentials_dev.yml` in the format: `"NGROK-URL/webhooks/slack/webhook"` for the `webhook_url`.

Afterward, execute the following commands:

### Terminal 2:

```bash
 rasa run --connector slack --credentials credentials-dev.yml --endpoints endpoints-dev.yml
 ```
### Terminal 3:
  ```bash
rasa run actions
 ```
