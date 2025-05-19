<template> 
    <header class="header">
        <div class="logo-container">
            <img src="../assets/images/logo-coppel.png" alt="Logo" class="logo" />
        </div>
        <div class="right-section">
            <div class="notifications-container">
                <button class="notification-btn" @click="toggleNotifications">
                    <i class="bell-icon">🔔</i>
                    <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
                </button>
                <div v-if="showNotifications" class="notifications-dropdown">
                    <div v-if="notifications.length === 0" class="empty-notifications">
                        No hay notificaciones
                    </div>
                    <div 
                        v-for="(notification, index) in notifications" 
                        :key="index" 
                        class="notification-item"
                        :class="{ 'unread': notification.unread }"
                    >
                        <div class="notification-content">
                            <p class="notification-text">{{ notification.message }}</p>
                            <small class="notification-time">{{ notification.time }}</small>
                        </div>
                        <button 
                            @click.stop="markAsRead(index)" 
                            class="mark-read-btn"
                            v-if="notification.unread"
                        >
                            ×
                        </button>
                    </div>
                </div>
            </div>
            <div class="user-info">
                <span class="username">{{ username }}</span>
                <i class="user-icon">👤</i>
            </div>
        </div>
    </header>
</template>

<script>
    export default {
        name: "Header",
        data() {
            return {
                username: 'Usuario: Adolfo',
                showNotifications: false,
                notifications: [],
                lastChecked: null
            };
        },
        computed: {
            unreadCount() {
                return this.notifications.filter(n => n.unread).length;
            }
        },
        methods: {
            toggleNotifications() {
                this.showNotifications = !this.showNotifications;
                if (this.showNotifications) {
                    this.checkForNotifications();
                }
            },
            async checkForNotifications() {
                try {
                    // Obtener activos con soporte o vida útil próximos a vencer
                    const response = await this.$axios.get('/api/activos/notificaciones');
                    const activosRiesgo = response.data;
                    
                    // Limpiar notificaciones antiguas
                    this.notifications = [];
                    
                    // Verificar activos con soporte próximo a vencer
                    if (activosRiesgo.soporte.length > 0) {
                        this.addNotification('Hay activos en riesgo de soporte');
                    }
                    
                    // Verificar activos con vida útil próxima a vencer
                    if (activosRiesgo.vida.length > 0) {
                        this.addNotification('Hay activos en riesgo de vida');
                    }
                    
                    // Guardar hora de última verificación
                    this.lastChecked = new Date();
                    
                } catch (error) {
                    console.error('Error al obtener notificaciones:', error);
                }
            },
            addNotification(message) {
                const now = new Date();
                this.notifications.unshift({
                    message,
                    time: now.toLocaleTimeString(),
                    date: now.toLocaleDateString(),
                    unread: true
                });
            },
            markAsRead(index) {
                this.notifications[index].unread = false;
            },
            closeNotifications(e) {
                if (!this.$el.contains(e.target)) {
                    this.showNotifications = false;
                }
            }
        },
        mounted() {
            // Verificar notificaciones cada 30 minutos
            this.checkForNotifications();
            setInterval(this.checkForNotifications, 30 * 60 * 1000);
            
            // Cerrar notificaciones al hacer clic fuera
            document.addEventListener('click', this.closeNotifications);
        },
        beforeDestroy() {
            document.removeEventListener('click', this.closeNotifications);
        }
    };
</script>

<style scoped>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ffe94b;
        padding: 0.3em 0.3em;
        position: relative;
    }
  
    .logo-container {
        display: flex;
        align-items: center;
    }
  
    .logo {
        width: 80px;
        height: 80px;
    }
  
    .right-section {
        display: flex;
        align-items: center;
        gap: 20px;
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

    /* Estilos para notificaciones */
    .notifications-container {
        position: relative;
    }

    .notification-btn {
        background: none;
        border: none;
        cursor: pointer;
        position: relative;
        padding: 5px;
    }

    .bell-icon {
        font-size: 24px;
    }

    .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background-color: #e74c3c;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    .notifications-dropdown {
        position: absolute;
        right: 0;
        top: 100%;
        width: 300px;
        max-height: 400px;
        overflow-y: auto;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }

    .empty-notifications {
        padding: 15px;
        text-align: center;
        color: #7f8c8d;
    }

    .notification-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        border-bottom: 1px solid #eee;
        background-color: #f9f9f9;
    }

    .notification-item.unread {
        background-color: #fff;
        font-weight: bold;
    }

    .notification-content {
        flex-grow: 1;
    }

    .notification-text {
        margin: 0;
        color: #2c3e50;
    }

    .notification-time {
        color: #7f8c8d;
        font-size: 0.8em;
    }

    .mark-read-btn {
        background: none;
        border: none;
        color: #7f8c8d;
        cursor: pointer;
        font-size: 1.2em;
        padding: 0 5px;
    }

    .mark-read-btn:hover {
        color: #e74c3c;
    }
</style>