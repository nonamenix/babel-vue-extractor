<template>
  <p>{{ _('Xin chào, Babel') }}</p>
</template>

<script>
  module.exports = {
    data: function() {
      return {
        intro: gettext('Tôi là một chú hươu nhỏ')
      }
    }
  }
</script>
