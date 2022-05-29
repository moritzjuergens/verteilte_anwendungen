<template>
  <div class="content">
    <h4>Question Number: {{ questionNr }}/{{ questions.length }}</h4>
    <h4>Correct Answers: {{ numCorrect }}/{{ numTotal }}</h4>
  </div>
</template>

<script>
export default {
  props: {
    questions: [],
    questionNr: Number,
    numCorrect: Number,
    numTotal: Number,
  },
};
</script>

<style>
.content {
  margin: 5%;
}
</style>
