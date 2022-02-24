<template>
    <div class="container" id="login-container">
        <div class="columns">
            <div class="column is-12">
                <h1 class="is-size-1">Log In</h1>
                <p>Welcome back! Please enter your details.</p>
            </div>
        </div>
        <div class="columns" v-if="error">
            <div class="column is-12">
                <b-message type="is-danger">
                    {{ error }}
                </b-message>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Username">
                    <b-input v-model="username"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Password">
                    <b-input v-model="password" type="password" password-reveal></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-button type="is-info" expanded @click="signIn()" :loading="isLoading">Sign in</b-button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    data() {
        return {
            isLoading: false,
            username: '',
            password: '',
            error: null
        }
    },
    methods: {
        ...mapActions(['login']),
        async signIn () {
            try {
                this.isLoading = true

                await this.login({
                    username: this.username,
                    password: this.password
                })

                this.$router.push("/")
                this.error = null
            } catch (err) {
                console.log(err);
                if (err.response.status === 400) {
                    this.error = 'Invalid Credentials. Please try again.'
                } else {
                    this.error = err.message
                }
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>

<style>
    #login-container {
        text-align: left;
        width: 400px;
        margin-top: 8em;
    }
</style>
