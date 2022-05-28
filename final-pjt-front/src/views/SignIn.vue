   <!-- <div>
    <h1>Login</h1>

    <account-error-list v-if="authError"></account-error-list>


    <form @submit.prevent="login(credentials)">
      <div>
        <label for="username">username: </label>
        <input v-model="credentials.username" type="text" id="username" required />
      </div>

      <div>
        <label for="password">password: </label>
        <input v-model="credentials.password" type="password" id="password" required />
      </div>

      <button>Login</button>
    </form>
  </div> -->

<template>
  <div>
    <div class="for-nav"></div>
    <div class="sign-in-form">
      <h1 style="color: rgba(240,240,240,1);" class="mb-5">LogIn</h1>

      <account-error-list v-if="authError"></account-error-list>

      <div class="form-box d-flex justify-content-center">
        <div class="form-content">
          <form @submit.prevent="login(credentials)" class="d-flex flex-column align-items-start my-1">
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="username" style="color: rgba(240,240,240,1);">Username: </label>
              <input  v-model="credentials.username" type="text" id="username" class="my-1" required/>
            </div>
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="password1" style="color: rgba(240,240,240,1);">Password: </label>
              <input v-model="credentials.password" type="password" id="password1" class="my-1" required />
            </div>
            <div class="d-flex form-item justify-content-end">
              <button class="my-1">LogIn</button> 
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  import AccountErrorList from '@/components/AccountErrorList.vue'

  export default {
    name: 'SignIn',
    components: {
      AccountErrorList,
    },
    data() {
      return {
        credentials: {
          username: '',
          password: '',
        }
      }
    },
  computed: {
      ...mapGetters(['authError'])
    },
    methods: {
      ...mapActions(['login'])
    },
  }
</script>

<style>
.sign-in-form{
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