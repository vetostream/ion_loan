import axios from '@/api/base'

const authUrl = `${process.env.VUE_APP_DJANGO_BASE}`

const state = {
    username: null,
};
const getters = {
    isAuthenticated: (state) => !!state.username,
};
const actions = {
    async login({ commit }, user) {
        await axios.get('set_csrf/')
        await axios.post('login/', user)
        const myself = await axios.get('check_session/')
        await commit('setUser', myself.data.user)
    },
    async logout({ commit }) {
        commit('setUser', null)
        await axios.post('logout/')
    }
};
const mutations = {
    setUser: (state, user) => state.username = user
};
export default {
  state,
  getters,
  actions,
  mutations
};
