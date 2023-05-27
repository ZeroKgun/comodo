<template>
  <div class="lecture">
    <div class="list-btn">
      <router-link
        tag="button"
        to="/lecture"
        class="list-btn__router"
      >
        <b-icon icon="list" to="/lecture"/> List
      </router-link>
    </div>
    <div class="lecture__header">
      <router-link :to="'/lecture/' + lecture.id">
        <div class="lecture__title" v-if="lecture">{{ lecture.title }}</div>
      </router-link>
      <div class="lecture__title">{{ lecture.title }}</div>
      <div class="lecture__date">{{ getTimeFormat(lecture.create_time) }}</div>
    </div>
    <div class="lecture__content" v-katex>
      <p v-dompurify-html="lecture.content" v-if="lecture" />
    </div>
    <b-list-group class="lecture__pagination">
      <b-list-group-item
        v-if="prevlecture !== null"
        id="lecture__pagination-item"
        :to="'/lecture/' + prevlecture.id"
      >
        <span class="pagination-text"><b-icon class="mr-2" icon="chevron-up"/>Previous</span>
        <span style="color: #696969">{{ prevlecture.title }}</span>
      </b-list-group-item>
      <b-list-group-item
        v-if="nextlecture !== null"
        id="lecture__pagination-item"
        :to="'/lecture/' + nextlecture.id"
      >
        <span class="pagination-text"><b-icon class="mr-2" icon="chevron-down"/>Next</span>
        <span style="color: #696969">{{ nextlecture.title }}</span>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import time from '@/utils/time'
import api from '@oj/api'

export default {
  name: 'lecture Details',
  data () {
    return {
      lecture: null,
      prevlecture: null,
      nextlecture: null,
      btnLoading: false
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      this.btnLoading = true;
      try {
        const res = await api.getLectureDetail(this.$route.params.lectureID); // API 요청을 보내서 선택한 글의 세부 정보를 가져옴
        this.btnLoading = false;
        this.lecture = res.data.data.current; // 선택한 글의 세부 정보를 변수에 저장
        this.prevlecture = 'previous' in res.data.data ? res.data.data.previous : null;
        this.nextlecture = 'next' in res.data.data ? res.data.data.next : null;
      } catch (err) {
        console.error('Failed to fetch lecture details:', err);
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    }
  },
  watch: {
    async '$route' () {
      await this.init()
    },
    immediate: true
  }
}
</script>

<style lang="scss">
  .lecture{
    margin: 0 20%;
  }
  .list-btn{
    margin-top: 100px;
    display: flex;
    justify-content: flex-end;
  }
  .list-btn__router{
    padding: 0.2em 0.6em;
    margin-bottom: 0.2em;
    border-radius: 8px;
    background: transparent;
    color: #7C7C7C;
    border: none;
    &:hover {
      background: #B8B8B8;
    }
  }
  .lecture__header{
    overflow: hidden;
    background: #F9F9F9;
    border-top: 2px solid #7C7C7C;
    border-bottom: 1px solid #B8B8B8;
    color: #7C7C7C;
  }
  .lecture__title{
    float: left;
    margin: 10px 1rem;
    font-size: 24px;
    font-weight: bold;
  }
  .lecture__date{
    float: right;
    margin: 12px 1rem;
    font-size: 20px;
    font-weight: 400;
    text-align: right;
  }
  .lecture__content{
    @import '@/styles/tiptapview.scss';
    margin: 30px 1rem;
    color: #696969;
  }
  .lecture__pagination{
    margin: 120px 0 24px;
    border-top: 2px solid #B8B8B8;
  }
  #lecture__pagination-item {
    border-bottom: 2px solid #B8B8B8;
    height: 50px;
  }
  .pagination-text{
    display: inline-block;
    width: 120px;
    margin: auto 20px;
    color: #696969;
  }
</style>
