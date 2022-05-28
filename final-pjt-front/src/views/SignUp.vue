<template>
  <div class="sign-up">
    <div class="for-nav"></div>
    <div class="sign-up-form">
      <h1 style="color: rgba(240,240,240,1);" class="mb-5">Signup</h1>

      <account-error-list v-if="authError"></account-error-list>

      <div class="form-box d-flex justify-content-center">
        <div class="form-content">
          <form @submit.prevent="signup(credentials)" class="d-flex flex-column align-items-start my-1">
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="username" style="color: rgba(240,240,240,1);">Username: </label>
              <input  v-model="credentials.username" type="text" id="username" class="my-1" required/>
            </div>
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="password1" style="color: rgba(240,240,240,1);">Password: </label>
              <input v-model="credentials.password1" type="password" id="password1" class="my-1" required />
            </div>
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="password2" style="color: rgba(240,240,240,1);">Password Confirmation:</label>
              <input v-model="credentials.password2" type="password" id="password2" class="my-1" required />
            </div>
            <div class="d-flex form-item justify-content-end">
              <button class="my-1">Signup</button> 
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  // import AccountErrorList from '@/components/AccountErrorList.vue'

  export default {
    name: 'SignUp',
    // components: {
    //   AccountErrorList,
    // },
    data() {
      return {
        credentials: {
          username: '',
          password1: '',
          password2: '',
        }
      }
    },
    computed: {
      ...mapGetters(['authError'])
    },
    methods: {
      ...mapActions(['signup'])
    },
  }
</script>

<style>
.sign-up-form{
  position: relative;
  top: 25vh;
}
.for-nav{
  height: 5em;
}
.form-item{
  width: 100%;
}
.form-content{
  width: 21%;
}

  
  </style>