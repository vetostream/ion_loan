<template>
    <div class="container is-fluid">
        <h1 class="has-text-left header">Clients</h1>
        <b-field>
            <b-input placeholder="Search Client Last Name"
                type="search"
                icon="search"
                @input="searchClient">
            </b-input>
        </b-field>
        <div class="table">
            <b-table :data="clients" :columns="clientTableColumns" :loading="isLoading" v-if="isSearching" @click="viewClient($event)" :selected.sync="selectedClient" focusable>
                <template #empty>
                    <div class="has-text-centered">No Results Found</div>
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
import { searchClients } from '@/api/client.js'

export default {
    name: 'Dashboard',
    data() {
        return {
            isLoading: false,
            isSearching: false,
            clients: [],
            clientTableColumns: [
                {
                    field: 'full_name',
                    label: 'Full Name'
                },
                {
                    field: 'birth_date',
                    label: 'Date of Birth'
                },
                {
                    field: 'active_loans',
                    label: 'Active Loans',
                    centered: true
                },
                {
                    field: 'active_cas',
                    label: 'Active Cash Advances',
                    centered: true
                }
            ],
            selectedClient: null,
        }
    },
    methods: {
        async searchClient(value) {
            if (value === "") {
                this.clients = []
                this.isSearching = false
            } else {
                this.isSearching = true
                try {
                    this.isLoading = true
                    const response = await searchClients(value)
                    this.clients = response.data.map(element => {
                        return {
                            ...element,
                            full_name: `${element.last_name}, ${element.first_name}`,
                            birth_date: element.birth_date,
                            active_loans: 0,
                            active_cas: 0
                        }
                    });
                    this.isLoading = false
                } catch (err) {
                    this.$buefy.toast.open({
                        message: `Something went wrong: ${err.message}`,
                        type: 'is-danger'
                    })
                }
            }
        },
        viewClient(row) {
            this.$router.push({ name: 'ClientDetail', params: { id: row.id } })
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
