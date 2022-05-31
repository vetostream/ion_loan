<template>
    <div class="container-fluid">
        <h1 class="is-size-4">
            Loan Masterlist
        </h1>
        <div class="columns">
            <div class="column is-half">
                <div class="columns mt-1">
                    <div class="column is-3">
                        <b-field label="Month">
                            <b-select placeholder="Select a month" expanded v-model="month">
                                <option
                                    v-for="option in months"
                                    :value="option.value"
                                    :key="option.value">
                                    {{ option.name }}
                                </option>
                            </b-select>
                        </b-field>
                    </div>
                    <div class="column is-3">
                        <b-field label="Year">
                            <b-input v-cleave="masks.dateField" placeholder="YYYY" v-model="year" id="filter-date"></b-input>
                        </b-field>
                    </div>
                </div>
                <div class="columns">
                    <div class="column is-6">
                        <b-button type="is-warning" expanded @click="generateReport">Generate Report</b-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Cleave from 'cleave.js'

const cleave = {
    name: 'cleave',
    bind(el, binding) {
        const input = el.querySelector('input')
        input._vCleave = new Cleave(input, binding.value)
    },
    unbind(el) {
        const input = el.querySelector('input')
        input._vCleave.destroy()
    }
}

export default {
    name: 'LoanMasterlist',
    directives: {
        cleave
    },
    data() {
        return {
            year: null,
            month: null,
            months: [
                {name: 'January', value: 1},
                {name: 'February', value: 2},
                {name: 'March', value: 3},
                {name: 'April', value: 4},
                {name: 'May', value: 5},
                {name: 'June', value: 6},
                {name: 'July', value: 7},
                {name: 'August', value: 8},
                {name: 'September', value: 9},
                {name: 'October', value: 10},
                {name: 'November', value: 11},
                {name: 'December', value: 12},
            ],
            masks: {
                dateField: {
                    date: true,
                    datePattern: ['Y'],
                }
            },
        }
    },
    methods: {
        generateReport() {
            window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/loan_masterlist/${this.year}/${this.month}/`)
        }
    }
}
</script>
