<template>
  <div class="notice-list-card font-bold">
    <div class="flex justify-between mr-32">
      <page-title text="게시판"/>
      <div class="my-auto h-8">
        <b-button
          v-if="!saveBtnVisible"
          size="sm"
          @click="openWriteForm"
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
      @row-clicked="goLecture"
    >
      <template v-slot:title="data">
        <a @click="goLecture(data.row)">{{ data.row.title }}</a>
      </template>
      <template v-slot:create_time="data">
        {{ getTimeFormat(data.row.create_time) }}
      </template>
      <template v-slot:top_fixed="data">
        <icon v-if="data.row.top_fixed===true" icon='thumbtack'/>
      </template>
      <div v-for="lecture in lectures" :key="lecture.id" @click="goLecture(lecture)">
        <!-- 글 목록을 렌더링하고, 각 글을 클릭했을 때 goLecture 메서드 호출 -->
      </div>
    </Table>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
    <b-modal v-model="showModal" title="글 작성" hide-footer :modal-class="'write-form'">

  <div class="d-flex flex-column">
    <div>
      <label for="lecture-title">제목:</label>
      <input v-model="newLecture.title" type="text" id="lecture-title" class="form-control" />
    </div>
    <div class="mt-3">
      <label for="lecture-content">내용:</label>
      <textarea v-model="newLecture.content" id="lecture-content" rows="10" class="form-control"></textarea>
    </div>
    <div class="mt-3 ml-auto">
      <b-button @click="savePost" variant="primary" class="mr-2">작성 완료</b-button>
      <b-button @click="cancelPost" variant="secondary" style="background-color: #7C7A7B; color: white;">취소</b-button>

    </div>
  </div>
</b-modal>

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
      showModal: false,
      newLecture: {
        title: '',
        content: ''
      },
      content: '', // 작성한 글을 저장하는 데이터 속성
      saveBtnVisible: false,
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
    await this.init();
    this.loadSavedLectures(); // 로컬 스토리지에서 데이터를 가져옵니다.
    this.fetchLectures(); // 컴포넌트가 마운트되면 글 목록을 가져오는 함수 호출
  },
  methods: {
    openWriteForm () {
      this.saveBtnVisible = false;
      this.newLecture.title = ''; // 제목 초기화
      this.newLecture.content = ''; // 내용 초기화
      this.showModal = true;
    },
    async fetchLectures () {
      try {
        const response = await api.getLectures(); // API 요청을 보내서 글 목록을 가져옴
        this.lectures = response.data; // 가져온 글 목록을 변수에 저장
      } catch (error) {
        console.error('Failed to fetch lectures:', error);
      }
    },
    savePost () {
      // 작성한 글을 게시판에 추가하는 로직을 작성합니다.
      // this.content 변수에 작성한 내용이 저장되어 있습니다.
      // 게시판의 데이터 배열에 새로운 항목을 추가하고, 필요한 처리를 수행합니다.
      // 필요한 경우 API를 호출하여 서버에 데이터를 전송할 수도 있습니다.

      // 예시: lectures 배열에 새로운 글 추가
      this.lectures.unshift({
        title: this.newLecture.title,
        create_time: new Date().toISOString()
        // 필요한 다른 속성들도 추가할 수 있습니다.
      });

      this.showModal = false; // 모달 창 닫기
      this.content = ''; // 작성 내용 초기화
      localStorage.setItem('lectures', JSON.stringify(this.lectures));
    },
    loadSavedLectures () {
      const savedLectures = localStorage.getItem('lectures');
      if (savedLectures) {
        this.lectures = JSON.parse(savedLectures);
      }
    },
    cancelPost () {
      this.showModal = false; // 모달 창 닫기
    },
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
    async goLecture (lecture) {
      this.lecture = lecture
      this.listVisible = false
      try {
        const res = await api.getLectureDetails(lecture.id); // 적절한 API 메소드를 사용하여 강의 내용을 가져옵니다
        this.lecture.content = res.data.content; // 강의 내용이 'content' 필드에 반환된다고 가정하고, 강의 객체를 해당 내용으로 업데이트합니다
      } catch (err) {
        console.error(err);
      }
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
.write-form .modal-content {
  width: 800px; /* 원하는 너비로 설정 */
  height: 600px; /* 원하는 높이로 설정 */
}
</style>
