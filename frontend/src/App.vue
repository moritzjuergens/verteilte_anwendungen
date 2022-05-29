<template>
  <div id="app">
    <Header />
    <div class="grid-container">
      <Counter
        :questions="questions"
        :questionNr="index + 1"
        :numCorrect="numCorrect"
        :numTotal="numTotal"
      />

      <div class="container">
        <div>
          <label for="name">Name:</label>
          <input type="text" name="name" id="name" v-model="player" />
        </div>
        <button id="highscore" @click="a = 1">Show Highscore</button>
      </div>
    </div>
    <QuestionBox
      :questionNr="index + 1"
      :currentQuestion="questions[index]"
      :next="next"
      :increment="increment"
      :numCorrect="numCorrect"
      :highscores="highscores"
      :player="player"
      :a="a"
    />
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import QuestionBox from "./components/QuestionBox.vue";
import Counter from "./components/Counter";

export default {
  name: "App",
  components: {
    Header,
    QuestionBox,
    Counter,
  },
  data() {
    return {
      questions: [],
      highscores: [],
      index: 0,
      numCorrect: 0,
      numTotal: 0,
      player: "",
      a: 0,
    };
  },
  methods: {
    next() {
      this.index++;
    },
    increment(isCorrect) {
      if (isCorrect) {
        this.numCorrect++;
      }
      this.numTotal++;
    },
  },
  mounted: function () {
    fetch("http://127.0.0.1:5000/questions", {
      method: "get",
    })
      .then((response) => {
        return response.json();
      })
      .then((jsonData) => {
        this.questions = jsonData;
        console.log(jsonData);
      });
    fetch("http://127.0.0.1:5000/highscores", {
      method: "get",
    })
      .then((response) => {
        return response.json();
      })
      .then((jsonData) => {
        this.highscores = jsonData;
        console.log(jsonData);
      });
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
.grid-container {
  display: grid;
  grid-template-columns: auto auto;
}
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>
