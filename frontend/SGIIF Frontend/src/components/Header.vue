<template> 
    <header class="header">
        <div class="logo-container">
            <img src="../assets/images/logo-coppel.png" alt="Logo" class="logo" />
        </div>
        <div class="user-info">
            <span class="username">{{ username }}</span>
            <i class="user-icon">👤</i>
        </div>
    </header>
</template>

<script>
    export default {
        name: "Header",
        data() {
            return {
            username: 'Usuario: Adolfo', // Aquí puedes obtener el nombre del usuario que inició sesión
      };
    },
    };
</script>

<style scoped>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffe94b;
        padding: 0.3em 0.3em;
    }
  
    .logo-container {
        display: flex;
        align-items: center;
    }
  
        .logo {
        width: 80px;
        height: 80px;
        }
  
    .user-info {
    display: flex;
    align-items: center;
    }
  
    .username {
        margin-right: 10px;
        font-size: 18px;
    }
  
    .user-icon {
        font-size: 24px;
    }
</style>