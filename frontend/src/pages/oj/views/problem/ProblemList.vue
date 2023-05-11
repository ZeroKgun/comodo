<template>
  <div>
    <!-- <page-top>
      <template #title>
        <span class="text-white"> Problems </span>
      </template>
      <template #description>
        알고리즘 분류와 난이도를 선택하여 지금 내게 필요한 문제를 풀어보세요!
      </template>
    </page-top> -->
    <div class="problem-list-card font-bold">
      <div v-for="problemSetGroup in problemSetGroups" :key="problemSetGroup.id">
        <h4 class="subtitle-blue text-xl">
          {{ problemSetGroup.title }}
        </h4>
        <problem-set-group :problem-set-group="problemSetGroup"></problem-set-group>
      </div>
      <h4 v-if="tag===''" class="subtitle-blue text-xl">
        All Problems
      </h4>
      <h4 v-else class="subtitle-blue text-xl">{{ tag }}</h4>
      <div class="mb-4 my-4">
        <div class="category-container d-flex">
          <div class="mr-auto">
            <b-dropdown text="Tag">
              <b-dropdown-item @click="filterByTag('')">전체</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('math')">수학</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('implementation')">구현</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('sorting')">정렬</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('string')">문자열</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('dp')">다이나믹 프로그래밍</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('dfs/bfs')">깊이/너비 우선 탐색</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('data_structures')">자료 구조</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('greedy')">그리디</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('bruteforcing')">브루트포스</b-dropdown-item>
              <b-dropdown-item @click="filterByTag('graph')">그래프</b-dropdown-item>
            </b-dropdown>
            <b-dropdown :text="difficulty" class="ml-3">
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('All')">All</b-dropdown-item>
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('Level1')">Level1</b-dropdown-item>
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('Level2')">Level2</b-dropdown-item>
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('Level3')">Level3</b-dropdown-item>
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('Level4')">Level4</b-dropdown-item>
              <b-dropdown-item class="ml-3 my-1" @click="filterByDifficulty('Level5')">Level5</b-dropdown-item>
            </b-dropdown>
          </div>
          <div class="tags mx-1">
            tags
            <b-form-checkbox
              v-model="checked"
              name="check-button"
              switch
              class="ml-2"
            >
            </b-form-checkbox>
          </div>
          <div class="col-3">
            <b-icon icon="search" class="search-icon"/>
            <b-input placeholder="keywords" class="search-input w-40"
              v-model="keyword" @input="filterByKeyword"/>
          </div>
        </div>
      </div>
      <div class="table">
        <b-table
          hover
          :items="problemList"
          :fields="problemTableColumns"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          @row-clicked="goProblem"
        >
          <template #cell(title)="data">
            {{data.value}}
            <b-icon icon="check2-circle" style="color: #B93234;" font-scale="1.2" v-if="data.item.my_status===0"></b-icon>
          </template>
          <template #cell(difficulty)="data">
            <b-icon
              icon="circle-fill"
              class="mr-2"
              :style="'color:' + difficultyColor(data.value)"
            />
            {{ data.value }}
          </template>
          <template #cell(AC_Rate)="data">
            {{ getACRate(data.item.accepted_number, data.item.submission_number) }}
          </template>
          <template v-slot:cell(tags)="data">
            <span v-show="checked" v-for="item in data.item.tags" :key="item.id">{{ item }}  </span>
          </template>
          <template v-slot:head(tags)="field">
            <div v-show="checked">{{ field.label }}</div>
          </template>
        </b-table>
      </div>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import { ProblemMixin } from '@oj/components/mixins'
import { DIFFICULTY_COLOR } from '@/utils/constants'
import ProblemSetGroup from '@oj/components/ProblemSetGroup.vue'
// import PageTop from '@oj/components/PageTop.vue'

export default {
  name: 'problemList',
  components: {
    ProblemSetGroup
    // PageTop
  },
  mixins: [ProblemMixin],
  data () {
    return {
      perPage: 20,
      currentPage: 1,
      checked: false,
      problemList: [],
      limit: 50,
      total: 0,
      keyword: '',
      difficulty: 'All',
      tag: '',
      page: 1,
      problemTableColumns: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: 'Title',
          key: 'title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          label: 'Level',
          key: 'difficulty',
          tdClass: 'levelCircle'
        },
        {
          label: 'Submissions',
          key: 'submission_number'
        },
        'AC_Rate',
        {
          label: 'Tags',
          key: 'tags'
        }
      ]
    }
  },
  computed: {
    rows () {
      return this.problemList.length
    },
    ...mapGetters(['isAuthenticated'])
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getTagList()
      await this.getProblemSetGroupList()
      await this.getProblemList()
    },
    async getProblemSetGroupList () {
      const res = await api.getProblemSetGroup()
      this.problemSetGroups = res.data.data
    },
    async getTagList () {
      const res = await api.getProblemTagList()
      this.tagList = res.data.data
    },
    async getProblemList () {
      const offset = (this.page - 1) * this.limit
      const res = await api.getProblemList(offset, this.limit,
        {
          difficulty: this.difficulty === 'All' ? '' : this.difficulty,
          keyword: this.keyword,
          tag: this.tag,
          page: this.page
        }
      )
      this.total = res.data.data.total
      this.problemList = res.data.data.results
      if (this.isAuthenticated) {
        this.addStatusColumn(this.problemTableColumns, res.data.data.results)
      }
    },
    async filterByDifficulty (item) {
      this.difficulty = item
      this.page = 1
      await this.getProblemList()
    },
    async filterByTag (item) {
      this.tag = item
      this.page = 1
      await this.getProblemList()
    },
    async filterByKeyword () {
      this.page = 1
      await this.getProblemList()
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
    async goProblem (item) {
      await this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    }
  },
  watch: {
    async 'isAuthenticated' (newVal) {
      await this.init()
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .subtitle-blue {
    color: #1A3E51;
    margin: 2rem 0 1rem 0;
  }
  .problem-list-card{
    margin:0 auto;
    width:70%;
    font-family:Manrope;
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  .category-container{
    display:flex;
    justify-content: flex-end;
  }
  .dropdown-toggle{
    margin-right:2em;
  }

  .custom-control{
    font-family: Manrope;
  }

  .tags{
    display: flex;
    align-items: center;
    font-family: Manrope;
    cursor: default;
  }
  [type=checkbox]:checked+label:before{
    background-color: #B93234 !important;
    border-color: #B93234 !important;
  }
  .problem-title-field{
    width: 25%;
  }

  .search-icon {
    position:absolute;
    top: 11px;
    left: 23px;
  }
  .search-input {
    margin-left: -5px;
    padding-left: 37px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  ::v-deep .table {
    width:100%;
    td {
      cursor: pointer;
    }
  }
  .tags {
    color:#767676;
  }
</style>
