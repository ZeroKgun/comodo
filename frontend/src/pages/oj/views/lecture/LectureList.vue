<template>
  <div class="notice-list-card font-bold">
    <div class="flex justify-between mr-32">
      <page-title text="게시판"/>
      <div class="my-auto h-8">
        <b-button
          v-if="!saveBtnVisible"
          size="sm"
          @click="window.open('/announcement/')"
        >글쓰기</b-button>
      </div>
    </div>
    <Table
      hover
      :items="lectures"
      :fields="lectureListField"
      :per-page="perPage"
      :current-page="currentPage"
      text="게시글이 없습니다"
      @row-clicked="golecture"
    >
      <template v-slot:title="data">
        {{data.row.title}}
      </template>
      <template v-slot:create_time="data">
        {{ getTimeFormat(data.row.create_time) }}
      </template>
      <template v-slot:top_fixed="data">
        <icon v-if="data.row.top_fixed===true" icon='thumbtack'/>
      </template>
    </Table>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import PageTitle from '@oj/components/PageTitle.vue'
import Table from '@oj/components/Table.vue'

export default {
  name: 'lecture',
  components: {
    PageTitle,
    Table
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      total: 10,
      btnLoading: false,
      lectures: [],
      lecture: '',
      listVisible: true,
      topFixedCount: 0,
      lectureListField: [
        {
          key: 'top_fixed',
          label: ''
        },
        { key: 'title' },
        {
          key: 'create_time',
          label: 'Date'
        }
      ]
    }
  },
  computed: {
    isContest () {
      return !!this.$route.params.contestID
    },
    rows () {
      return this.lectures.length
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      if (this.isContest) {
        await this.getContestlectureList()
      } else {
        await this.getlectureList()
      }
    },
    async getlectureList () {
      this.btnLoading = true
      try {
        const res = await api.getlectureList(0, 250)
        this.btnLoading = false
        const lectures = res.data.data.results
        const topFixed = lectures.filter(
          (lecture) => lecture.top_fixed === true
        )
        this.topFixedCount = topFixed.length
        const notTopFixed = lectures.filter(
          (lecture) => lecture.top_fixed === false
        )
        this.lectures = [...topFixed, ...notTopFixed]
        this.total = res.data.data.total
      } catch (err) {
        this.btnLoading = false
      }
    },
    async getContestlectureList () {
      this.btnLoading = true
      try {
        const res = await api.getContestlectureList(this.$route.params.contestID)
        this.btnLoading = false
        this.lectures = res.data.data
      } catch (err) {
        this.btnLoading = false
      }
    },
    async golecture (lecture) {
      this.lecture = lecture
      this.listVisible = false
      await this.$router.push({
        name: 'lecture-details',
        params: { lectureID: lecture.id }
      })
    },
    changeRowColor (lecture) {
      lecture._rowVariant = 'secondary'
    },
    calculateIdx (row) {
      return row.index - this.topFixedCount + 1
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    }
  }
}
</script>

<style lang="scss" scoped>
@font-face {
  font-family: Manrope_bold;
  src: url("../../../../fonts/Manrope-Bold.ttf");
}
.notice-list-card {
  margin: 0 auto;
  width: 70%;
  font-family: Manrope;
}
.no-lecture {
  text-align: center;
  font-size: 16px;
  margin: 10px 0;
}
.pagination {
  margin-right: 5%;
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.notice-title-field {
  width: 75%;
}
.font-bold {
  font-family: manrope_bold;
}
</style>

<!--template>
  <div class="lecture-list-card font-bold">
    <div class="flex justify-between mr-32">
      <page-title text="게시판"/>
      <div class="my-auto h-8">
        <b-button
          v-if="!saveBtnVisible"
          size="sm"
          @click="setBookmark"
        >All Course</b-button>
        <b-button
          v-if="saveBtnVisible"
          size="sm"
          @click="saveBookmark"
        >
          <b-icon icon="check"/> 저장
        </b-button>
      </div>
    </div>
    <div class="no-lecture" v-if="!lectureList.length">게시글이 없습니다</div>
    <div class="lecture-card-list">
      <b-card
        v-for="(lecture,index) in lectureList"
        :key="index"
        style="width: 230px; margin: 25px 25px 0 0; cursor: pointer;"
      >
        <b-card-text class="lecture-card__card">
          <div
            class="lecture-card__cardcolor"
            :style="'background-color:' + backcolor[index % 7]"
          ></div>
          <div class="lecture-card__lectureInfo">
            <div class="lecture-card__title">
              {{ lecture.course.title }}
              <b-button
                class="lecture-card__btn"
                @click="setBookmarkCourse(index, lecture.course.id, lecture.bookmark)"
                v-if="saveBtnVisible"
              >
                <b-icon :icon="setIcon(lecture.bookmark)"/>
              </b-button>
            </div>
            <div class="lecture-card__info">
              {{ lecture.course.course_code + '-' + lecture.course.class_number }}
              <span v-if="lecture.course.created_by.real_name">{{ '(' + lecture.course.created_by.real_name + ')' }} </span><br/>
              {{ lecture.course.registered_year + ' ' + getSemester(lecture.course.semester) }} <br/>
            </div>
            <div>
              <b-button
                class="lecture-card__btn mr-3"
                size="sm"
                v-b-tooltip.hover.bottomright="'Assignment'"
                :to="'lecture/' + lecture.course.id + '/assignment'">
                <b-icon icon="journal-text"/>
              </b-button>
              <b-button
                class="lecture-card__btn"
                size="sm"
                v-b-tooltip.hover.bottomright="'QnA'"
                :to="'lecture/' + lecture.course.id + '/question'">
                <b-icon icon="patch-question"/>
              </b-button>
            </div>
          </div>
        </b-card-text>
      </b-card>
    </div>
  </div>
</!--template>

<script>
import api from '@oj/api'
import PageTitle from '@oj/components/PageTitle.vue'

export default {
  name: 'CourseList',
  components: {
    PageTitle
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      lectureList: [],
      lectureTableColumns: [
        {
          label: 'Subject',
          key: 'course.title'
        },
        'Semester'
      ],
      semesters: ['Spring', 'Summer', 'Fall', 'Winter'],
      backcolor: [
        '#9EC1CF', '#CC99C9', '#FEB144', '#FF6663', '#7C7A7B', '#E2E2E2'
      ],
      saveBtnVisible: false
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      try {
        const resp = await api.getBookmarkCourseList()
        const data = resp.data.data
        this.lectureList = data.results
      } catch (err) {
      }
    },
    async goCourseDashboard (item) {
      await this.$router.push({
        name: 'lecture-dashboard',
        params: { courseID: item.course.id }
      })
    },
    async goAssignmentList (courseID) {
      await this.$router.push({
        name: 'lecture-assignment',
        params: {
          courseID: courseID
        }
      })
    },
    async setBookmark () {
      const resp = await api.getCourseList()
      const data = resp.data.data
      this.lectureList = data.results
      this.saveBtnVisible = true
    },
    async setBookmarkCourse (index, courseID, bookmark) {
      await api.setBookmark(courseID, !bookmark)
      this.lectureList[index].bookmark = !bookmark
    },
    async saveBookmark () {
      this.saveBtnVisible = !this.saveBtnVisible
      await this.init()
    },
    setIcon (bookmark) {
      return bookmark ? 'bookmark-fill' : 'bookmark'
    },
    getSemester (semesterno) {
      return this.semesters[semesterno]
    }
  },
  computed: {
  }
}
</script>

<style-- lang="scss" scoped>
  .font-bold {
    font-family: manrope_bold;
  }
  .lecture-list-card{
    margin:0 auto;
    width:70%;
  }
  .no-lecture {
    text-align: center;
  }
  .lecture-card-list {
    display: flex;
    flex-wrap: wrap;
    margin-left: 68px;
  }
  .card-body {
    padding: 0 !important;
  }
  .lecture-card {
    &__card ::v-deep{
      color: #7C7A7B;
      cursor: default;
    }
    &__cardcolor {
      height: 135px;
      border-radius: 8px 8px 0 0;
    }
    &__lectureInfo {
      padding: 25px;
    }
    &__title {
      font-size: 16px;
      display: flex;
      justify-content: space-between;
      word-break: keep-all;
    }
    &__info {
      margin-bottom: 10px;
      font-size: 12px;
    }
    &__btn ::v-deep {
      background-color: transparent;
      color: #7A7C7B;
    }
    &__btn:hover, __btn:active ::v-deep{
      background-color: transparent;
      color: #AAAAAA;
    }
  }
</style-->
