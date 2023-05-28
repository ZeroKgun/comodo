<template>
  <div class="hint">
    <b-button v-if="step === 0"
      v-b-modal.modal-multi-1 id="popover-target" class="bg-warning">Hint
    </b-button>
    <b-button v-else-if="step === 1"  @click="$bvModal.show('modal-multi-2')"
      v-b-modal.modal-multi-2 id="popover-target" class="bg-warning">Hint
    </b-button>
    <b-button v-else-if="step === 2"  @click="$bvModal.show('modal-multi-3')"
      v-b-modal.modal-multi-3 id="popover-target" class="bg-warning">Hint
    </b-button>
    <b-button v-else-if="step === 3"  @click="$bvModal.show('modal-multi-4')"
      v-b-modal.modal-multi-4 id="popover-target" class="bg-warning">Hint
    </b-button>
    <b-button v-else-if="step === 4"  @click="$bvModal.show('modal-multi-5')"
      v-b-modal.modal-multi-5 id="popover-target" class="bg-warning">Hint
    </b-button>
      <b-popover target="popover-target" triggers="hover" placement="bottomright">
        <template #title>Hint</template>
        <p class="my-1"><strong>1단계</strong>: <span class="text-danger">알고리즘 분류(Tag)</span> 공개</p>
        <p class="my-1"><strong>2단계</strong>: <span class="text-danger">사용 변수, 함수 인자</span> 공개</p>
        <p class="my-1"><strong>3단계</strong>: <span class="text-danger">의사 코드(Pseudo-code)</span> 공개</p>
        <p class="my-1"><strong>4단계</strong>: <span class="text-danger">해답</span> 공개</p>
      </b-popover>

    <b-modal id="modal-multi-1" title="Hint" @ok="$bvModal.show('modal-multi-2')" no-stacking>
      <p class="my-2">1단계 힌트를 보시겠습니까?</p>
      <b-button v-b-modal.modal-multi-2 @click="hintShowed()">1단계 힌트 보기</b-button>
    </b-modal>
    <b-modal id="modal-multi-2" title="1단계 힌트" no-stacking ok-only>
      <p class="my-2">Algorithm Tag: <span class="text-danger">{{ (tag || '').toUpperCase() }}</span></p>
      <b-button v-b-modal.modal-multi-3 @click="getGPTResponse(secondHint)">다음 단계 힌트 보기</b-button>
      <!-- <p v-else>{{ GPTResponseResult }}</p> -->
    </b-modal>
    <b-modal id="modal-multi-3" size="lg" title="2단계 힌트" no-stacking ok-only>
      <span v-if="showLoadingCircle"> L O A D I N G ... </span>
      <p v-else id="hint-message" v-html="renderedCodeBlock"></p>
      <b-button v-if="showHintButton" @click="getGPTResponse(thirdHint), $bvModal.show('modal-multi-4')">다음 단계 힌트 보기</b-button>
    </b-modal>
    <b-modal id="modal-multi-4" size="lg" title="3단계 힌트" no-stacking ok-only>
      <span v-if="showLoadingCircle"> L O A D I N G ... </span>
      <p v-else id="hint-message">{{ GPTResponseResult }}</p>
      <b-button v-if="showHintButton" @click="getGPTResponse(fourthHint), $bvModal.show('modal-multi-5')">다음 단계 힌트 보기</b-button>
    </b-modal>
    <b-modal id="modal-multi-5" size="lg" title="4단계 힌트" no-stacking ok-only>
      <span v-if="showLoadingCircle"> L O A D I N G ... </span>
      <p v-else id="hint-message" v-html="renderedCodeBlock"></p>
    </b-modal>
  </div>
</template>

<script>
import fetch from 'node-fetch'
import { marked } from 'marked'

export default {
  name: 'Hint',
  data () {
    return {
      step: 0,
      showHintButton: true,
      showLoadingCircle: false,
      GPTResponseResult: "",
      secondHint: '이 문제에 사용되는 변수와 함수 인자를 알려줘 "변수: ~~ 함수 인자: ~~ " 형태로 간단히 보여줘 정답은 보여주지 마',
      thirdHint: '이 문제 해답의 pseudo-code를 알려줘 in KOREAN, 정답 코드는 보여주지 마',
      fourthHint: '이 문제 정답 코드만 보여줘 마크다운 코드 블록 형식으로 보여줘'
    }
  },
  props: {
    tag: String,
    problemDesc: String,
    language: String
  },
  async mounted () {
  },
  computed: {
    renderedCodeBlock () {
      // 마크다운 코드 블록을 HTML로 변환
      const html = marked(this.GPTResponseResult);
      return html;
    },
    processedDesc: function () {
      return this.problemDesc.replace(/(<([^>]+)>)/gi, "")
    }
  },
  methods: {
    hintShowed () {
      this.step++
      console.log(this.step)
    },
    getGPTResponse (message) {
      this.hintShowed()
      console.log('!!' + this.problemDesc)
      this.showLoadingCircle = true
      this.showHintButton = false
      let question = `${this.processedDesc} \n ${message}`
      if (this.step === 4) {
        question += ` 사용 언어는 ${this.language}`
      }
      console.log(question)
      fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          // eslint-disable-next-line no-undef
          Authorization: "Bearer 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",
          'Content-Type': 'application/json',
          model: 'gpt-3.5-turbo'
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [{ role: 'user', content: question }]
        })
      })
        .then((res) => res.json())
        .then((data) => {
          this.showLoadingCircle = false
          this.showHintButton = true
          // string 예쁘게 보이게 처리해야함
          const responseText = data.choices[0].message.content
          const formattedText = responseText.replace(/\\n/g, '<br />')
          this.GPTResponseResult = formattedText
          console.log(this.GPTResponseResult)
        })
        .catch(err => console.warn(err))
    }
  }
}
</script>

<style lang="scss" scoped>
  #hint-message {
    white-space:pre-wrap;
  }
</style>
