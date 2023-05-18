
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
      <div class="lecture__title">{{ lecture.title }}</div>
      <div class="lecture__date">{{ getTimeFormat(lecture.create_time) }}</div>
    </div>
    <div class="lecture__content" v-katex>
      <p v-dompurify-html="lecture.content"/>
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
      this.btnLoading = true
      try {
        const res = await api.getlectureDetail(this.$route.params.lectureID)
        this.btnLoading = false
        this.lecture = res.data.data.current
        this.prevlecture = 'previous' in res.data.data ? res.data.data.previous : null
        this.nextlecture = 'next' in res.data.data ? res.data.data.next : null
      } catch (err) {
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    }
  },
  watch: {
    async '$route' () {
      await this.init()
    }
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

<!--template>
  <div class="dashboard-list-card font-bold">
    <div class="mb-5">
      <h5 class = "title"> {{ lecture.title }}_{{lecture.course_code}} </h5>
    </div>
    <b-row class="mt-5">
    <b-col cols = "8">
    <b-calendar block
      v-model="value"
      class="border rounded p-2 calendar"
      :date-info-fn="dateClass"
      @context="onContext"
      selected-variant="success"
      nav-button-variant="secondary"
      locale="en"
      ></b-calendar>
    </b-col>
    <b-col>
      <b-card :title= "value" class = "card h-100">
        <b-button v-if = assignmentExists() class ="AssignmentName w-100" @click="goAssignmentDetail(assignmentFind().id)" variant = "outline-light">
          {{ assignmentFind().title }}
        </b-button>
      </b-card>
    </b-col>
    </b-row>
    <b-row class = "mt-5 justify-content-center">
      <b-col cols = "6">
        <b-button class = "w-100 AssignmentsButton" @click="goAssignments" >Go to Assignments page</b-button>
      </b-col>
    </b-row>
  </div>
</!--template>

<script>
import api from '@oj/api'
export default {
  name: 'CourseDashboard',
  components: {
    // Split into many components
  },
  data () {
    return {
      value: '',
      courseID: '',
      context: '',
      lecture: {
        title: '',
        course_code: '',
        class_number: '',
        registered_year: '',
        semester: '',
        created_by: ''
      },
      assignment: [],
      datepick: [],
      assignmentnums: [],
      assignmentflag: false
    }
  },
  async mounted () {
    try {
      this.$Loading.start()
      this.courseID = this.$route.params.courseID
      const res = await api.getCourse(this.courseID)
      this.$Loading.finish()
      this.lecture = res.data.data.course
      const res2 = await api.getCourseAssignmentList(this.courseID)
      this.assignment = res2.data.data.results
    } catch (err) {
    }
  },
  methods: {
    async goAssignments () {
      await this.$router.push({
        name: 'lecture-assignment'
      })
    },
    async goAssignmentDetail (id) {
      await this.$router.push({
        name: 'lecture-assignment-detail',
        params: { courseID: this.courseID, assignmentID: id }
      })
    },
    dateClass (ymd, date) {
      const moment = require('moment')
      for (var i in this.assignment) {
        this.assignmentnums.push(i)
        this.datepick.push(moment(date).isBetween(this.assignment[i].start_time, this.assignment[i].end_time) ? date : '')
      }
      for (var j in this.datepick) {
        if (moment(this.datepick[j]).isSame(date)) {
          return 'AssignmentDates'
        }
      }
    },
    onContext (ctx) {
      this.context = ctx
    },
    assignmentFind () {
      const moment = require('moment')
      for (var i in this.datepick) {
        if (moment(this.datepick[i]).isSame(this.value)) {
          return this.assignment[this.assignmentnums[i]]
        }
      }
    },
    assignmentExists () {
      const moment = require('moment')
      var flag = false
      for (var i in this.datepick) {
        if (moment(this.datepick[i]).isSame(this.value)) {
          flag = true
          return true
        }
      }
      if (flag === false) {
        return false
      }
    }
  },
  computed: {
  }
}
</script>

<style-- lang="scss" scoped>
  .card {
    background-color: lightgray;
    box-shadow: none;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .title {
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
  }
  .dashboard-list-card {
    margin:0 auto;
    width:70%;
  }
  .calendar::v-deep .form-control {
    width:100%;
    box-shadow: none;
  }
  .calendar::v-deep .b-calendar-grid {
    width:100%;
    box-shadow: none;
  }
  .calendar::v-deep .btn {
    background-color: white;
    color: #4f4f4f;
  }
  .QnAButton {
    background-color: #E9A05A;
    &:hover{
      background-color: #b97f48;
    }
  }
  .AssignmentsButton {
    background-color: #3391E5;
    &:hover{
      background-color: #276fad;
    }
  }
  .AssignmentName {
    background-color: white;
    color : #4f4f4f;
    box-shadow: 0 0 0 1px #4f4f4f;
    &:hover{
      background-color: #c4c4c4;
    }
  }
  .calendar::v-deep .AssignmentDates{
    border-bottom-width: 5px;
    border-bottom-style: solid;
    position: relative;
    border-bottom-color: #B93234;
  }
  .button {
    cursor: pointer;
  }

</style-->
