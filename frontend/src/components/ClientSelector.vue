<template>
    <b-field label="Client" label-position="inside">
        <b-autocomplete
            :data="clients"
            :loading="isFetching"
            placeholder="Last Name"
            icon="search"
            field="pretty_result"
            @input="getAsyncData"
            @select="option => {$emit('client-selected', option)}">
            <template #empty>No results found</template>
        </b-autocomplete>
    </b-field>
</template>

<script>
import { searchClients } from '@/api/client.js'
import debounce from 'lodash/debounce'

export default {
    name: 'ClientSelector',
    data() {
        return {
            clients: [],
            isFetching: false,
        }
    },
    props: {
        selectedClient: {
            type: Object,
        }
    },
    methods: {
        getAsyncData: debounce(function (lastname) {
            if (!lastname.length) {
                this.clients = []
                return
            }
            this.isFetching = true
            searchClients(lastname)
                .then(({ data }) => {
                    this.clients = []
                    this.clients = data.map(element => {
                        return {
                            ...element,
                            pretty_result: `${element.last_name}, ${element.first_name} (${element.birth_date})`
                        }
                    })
                })
                .catch((error) => {
                    this.clients = []
                    throw error
                })
                .finally(() => {
                    this.isFetching = false
                })
        }, 500),
    }
}
</script>

<style>

</style>