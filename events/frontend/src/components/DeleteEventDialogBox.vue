<template>
  <v-dialog v-model="dialog" width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn class="mx-1" v-bind="attrs" v-on="on">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title>
        Delete Confirmation
      </v-card-title>

      <v-card-text>
        Are you certain you want to delete this event?
        <br>
        <br>
        This is a merciless operation.
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="triggerDelete">
          Yes
        </v-btn>
        <v-btn color="primary" text @click="dialog = false">
          No
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DeleteEventDialogBox",
  data() {
    return {
      dialog: false
    };
  },
  methods: {
    triggerDelete() {
      this.$emit("delete-confirmation");
      this.dialog = false;
    }
  }
};
</script>
