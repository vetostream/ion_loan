<template>
    <div class="container is-fluid">
        <div v-if="selectedLoan">
            <b-breadcrumb
                separator="has-arrow-separator"
            >
                <b-breadcrumb-item @click="resetView()">{{ header }}</b-breadcrumb-item>
                <b-breadcrumb-item active>Loan Detail</b-breadcrumb-item>
            </b-breadcrumb>
            <LoanDetail :selected_loan="selectedLoan" :is_approved="loan_status === 'approved'"/>
        </div>
        <div v-else>
            <h1 class="has-text-left header">{{ header }}</h1>
            <b-field>
                <b-input placeholder="Search Client Last Name"
                    type="search"
                    icon="search"
                    @input="searchLoans">
                </b-input>
            </b-field>
            <div class="table">
                <b-table :data="loans" :columns="columns" :loading="isLoading" v-if="isSearching" :selected.sync="selectedLoan" focusable>
                    <template #empty>
                        <div class="has-text-centered">No Results Found</div>
                    </template>
                </b-table>
            </div>
        </div>
    </div>
</template>

<script>
import { searchLoans } from '@/api/loan.js'
import LoanDetail from '@/components/LoanDetail.vue'

export default {
    name: 'LoanList',
    props: {
        loan_status: String,
        selectedLoan: Object,
        loans: []
    },
    components: {
        LoanDetail
    },
    data() {
        return {
            isLoading: false,
            isSearching: false,
            columns: [
                {
                    field: 'id',
                    label: 'ID'
                },
                {
                    field: 'principal_amount',
                    label: 'Principal Amount'
                },
                {
                    field: 'term',
                    label: 'Terms'
                },
                {
                    field: 'interest',
                    label: 'Interest'
                },
                {
                    field: 'client_display',
                    label: 'Full Name (DOB)'
                },
                {
                    field: 'control_number',
                    label: 'Control Number',
                },
            ]
        }
    },
    computed: {
        header () {
            switch(this.loan_status) {
                case 'pending':
                    return 'Pending Loans'
                case 'approved':
                    return 'Approved Loans'
                case 'declined':
                    return 'Declined Loans'
                default:
                    return 'Loans';
            }
        }
    },
    methods: {
        async searchLoans(value) {
            if (value === "") {
                this.loans = []
                this.isSearching = false
            } else {
                this.isSearching = true
                try {
                    this.isLoading = true

                    const params = {
                        client_last_name: value,
                        loan_status: this.loan_status
                    }

                    const response = await searchLoans(params)
                    this.loans = response.data.map(element => {
                        return {
                            id: element.id,
                            loan_type: element.loan_type,
                            full_name: element.client_full_name,
                            birth_date: element.client_birth_date,
                            date_created: element.date_created,
                            principal_amount: element.principal_amount,
                            term: element.term,
                            interest: element.interest,
                            start_payment: element.start_payment,
                            fee_others: element.fee_others,
                            client_display: `${element.client_full_name} (${element.client_birth_date})`,
                            is_advance: element.is_advance,
                            udi: element.udi,
                            gross_cash_out: element.gross_cash_out,
                            llrf: element.llrf,
                            processing_fee: element.processing_fee,
                            net_cash_out: element.net_cash_out,
                            control_number: element.control_number
                        }
                    });
                    this.isLoading = false
                } catch (err) {
                    console.log(err)
                    this.$buefy.toast.open({
                        message: `Something went wrong: ${err.message}`,
                        type: 'is-danger'
                    })
                }
            }
        },
        resetView () {
            this.loans = []
            this.isSearching = false
            this.selectedLoan = null
        }
    }
}
</script>

<style>
 .table {
     text-align: initial;
     margin-top: 1.5em;
 }
</style>
