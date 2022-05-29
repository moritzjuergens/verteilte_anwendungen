<template>
  <div>
    <b-container>
      <div class="m-jumbo">
        <div class="m-jumbo-header">{{ currentQuestion.question }}</div>
        <div class="m-jumbo-content">
          <b-list-group>
            <b-list-group-item
              v-for="(answer, index) in shuffledAnswers"
              :key="index"
              @click.prevent="selectAnswer(index)"
              :class="answerClass(index)"
              >{{ answer }}</b-list-group-item
            >
          </b-list-group>
        </div>
        <button
          id="submit"
          @click="submitAnswer"
          :disabled="selectedIndex === null || answered"
          :if="questionNr != 10"
        >
          Submit
        </button>
        <button id="next" @click="next" v-if="questionNr != 10">Next</button>
        <button
          id="submitScore"
          @click="submitScore"
          v-if="questionNr == 10"
          :disabled="player.length == 0 || player == null"
        >
          Submit Score
        </button>
      </div>
      <div class="m-jumbo" v-if="a == 1">
        <h2>Highscore</h2>
        <table>
          <tr>
            <td>Name</td>
            <td>Score</td>
          </tr>
          <tr v-for="(highscore, index) in highscores" :key="index">
            <td>{{ highscore.name }}</td>
            <td>{{ highscore.score }}</td>
          </tr>
        </table>
      </div>
    </b-container>
  </div>
</template>

<script>
import _ from "lodash";
export default {
  props: {
    questionNr: Number,
    currentQuestion: Object,
    next: Function,
    increment: Function,
    numCorrect: Number,
    highscores: Array,
    player: String,
    a: Number,
  },
  data() {
    return {
      selectedIndex: null,
      correctIndex: null,
      shuffledAnswers: [],
      answered: false,
    };
  },
  computed: {
    answers() {
      let answers = [...this.currentQuestion.incorrect_answers];
      answers.push(this.currentQuestion.correct_answer);
      return answers;
    },
  },
  watch: {
    currentQuestion: {
      immediate: true,
      handler() {
        this.selectedIndex = null;
        this.shuffleAnswers();
        this.answered = false;
      },
    },
  },
  methods: {
    selectAnswer(index) {
      console.log(index);
      this.selectedIndex = index;
    },
    shuffleAnswers() {
      let answers = [
        ...this.currentQuestion.incorrect_answers,
        this.currentQuestion.correct_answer,
      ];
      this.shuffledAnswers = _.shuffle(answers);
      this.correctIndex = this.shuffledAnswers.indexOf(
        this.currentQuestion.correct_answer
      );
    },
    submitAnswer() {
      let isCorrect = false;

      if (this.selectedIndex === this.correctIndex) {
        isCorrect = true;
      }
      this.increment(isCorrect);
      this.answered = true;
    },
    answerClass(index) {
      let answerClass = "";
      if (!this.answered && this.selectedIndex === index) {
        answerClass = "selected";
      } else if (this.answered && this.correctIndex === index) {
        answerClass = "correct";
      } else if (
        this.answered &&
        this.selectedIndex === index &&
        this.correctIndex !== index
      ) {
        answerClass = "wrong";
      }
      return answerClass;
    },
    submitScore() {
      (async () => {
        const rawResponse = await fetch("http://127.0.0.1:5000/results", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ player: this.player, score: this.numCorrect }),
        });
        const content = await rawResponse.json();
        console.log(content);
      })();
    },
  },
};
</script>

<style scoped>
.m-jumbo {
  width: 80vw;
  height: fit-content;
  background-color: azure;
  border: grey 1px solid;
  border-radius: 10px;
  box-shadow: 4px 4px 5px lightgrey;
  margin: auto;
  margin-top: 5%;
  padding: 2%;
  /* display: flex;
  justify-content: center;
  align-items: center; */
}

.m-jumbo-header {
  font-size: 3vw;
  margin: 2% auto;
  font-weight: bold;
}
.m-jumbo-content {
  margin: auto 5%;
}
.list-group-item:hover {
  background-color: #eee;
  cursor: pointer;
}
.selected {
  background-color: lightskyblue;
}
.correct {
  background-color: greenyellow;
}
.wrong {
  background-color: indianred;
}
#submit {
  margin: 3%;
  background-color: greenyellow;
  border: 1px solid black;
  border-radius: 5px;
  height: 10%;
  width: 15%;
}
#next {
  margin: 3%;
  background-color: lightskyblue;
  border: 1px solid black;
  border-radius: 5px;
  height: 10%;
  width: 15%;
}
#next:active {
  background-color: rgb(106, 162, 197);
}
#submit:active {
  background-color: rgb(132, 196, 36);
}
</style>
