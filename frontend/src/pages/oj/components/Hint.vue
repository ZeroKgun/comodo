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
    <b-modal id="modal-multi-2" title="1단계 힌트" ok-only>
      <p class="my-2">Algorithm Tag: <span class="text-danger">{{ tag.toUpperCase() }}</span></p>
      <b-button v-b-modal.modal-multi-3>다음 단계 힌트 보기</b-button>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'Hint',
  data () {
    return {
    }
  },
  props: ['tag'],
  async mounted () {
  },
  methods: {
  }
}
</script>
