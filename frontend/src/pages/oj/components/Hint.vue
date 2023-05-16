<template>
  <div class="hint">
    <b-button v-b-modal.modal-multi-1 id="popover-target-1" class="bg-warning">Hint</b-button>
      <b-popover target="popover-target-1" triggers="hover" placement="bottomright">
        <template #title>Hint</template>
        <p class="my-1"><strong>1단계</strong>: <span class="text-danger">알고리즘 분류(Tag)</span> 공개</p>
        <p class="my-1"><strong>2단계</strong>: <span class="text-danger">사용 변수, 함수 인자</span> 공개</p>
        <p class="my-1"><strong>3단계</strong>: <span class="text-danger">의사 코드(Pseudo-code)</span> 공개</p>
        <p class="my-1"><strong>4단계</strong>: <span class="text-danger">해답</span> 공개</p>
      </b-popover>
    <b-modal id="modal-multi-1" title="Hint" @ok="$bvModal.show('modal-multi-2')" no-stacking>
      <p class="my-2">1단계 힌트를 보시겠습니까?</p>
      <b-button v-b-modal.modal-multi-2>1단계 힌트 보기</b-button>
    </b-modal>
    <b-modal id="modal-multi-2" title="1단계 힌트" no-stacking ok-only>
      <p class="my-2">Algorithm Tag: <span class="text-danger">{{ tag.toUpperCase() }}</span></p>
      <b-button v-b-modal.modal-multi-3 @click="getGPTResponse()">다음 단계 힌트 보기</b-button>
      <!-- <p v-else>{{ GPTResponseResult }}</p> -->
    </b-modal>
    <b-modal id="modal-multi-3" title="2단계 힌트" ok-only>
      <span v-if="showLoadingCircle"> L O A D I N G ... </span>
      <p v-else>{{ GPTResponseResult }}</p>
    </b-modal>
  </div>
</template>

<script>
import fetch from 'node-fetch'

export default {
  name: 'Hint',
  data () {
    return {
      showHintButton: true,
      showLoadingCircle: false,
      GPTResponseResult: ""
    }
  },
  props: {
    tag: String,
    problemDesc: String
  },
  async mounted () {
  },
  methods: {
    getGPTResponse () {
      console.log(this.problemDesc)
      this.showLoadingCircle = true
      this.showHintButton = false;
      fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          // eslint-disable-next-line no-undef
          Authorization: `Bearer ${process.env.VUE_APP_OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
          model: 'gpt-3.5-turbo'
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [{ role: 'user', content: `${this.problemDesc} \n 이 문제 풀어줘` }]
        })
      })
        .then((res) => res.json())
        .then((data) => {
          this.showLoadingCircle = false;
          // string 예쁘게 보이게 처리해야함
          this.GPTResponseResult = data.choices[0].message.content
          console.log(this.GPTResponseResult)
        })
        .catch(err => console.warn(err))
    }
  }
}
</script>
