import axios from 'axios';

export default axios.create({
    baseURL: process.env.VUE_APP_API_ENDPOINT_URL,
    xsrfHeaderName: "X-CSRFToken",
    xsrfCookieName: 'csrftoken',
    withCredentials: true
});
