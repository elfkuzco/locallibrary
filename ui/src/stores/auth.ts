import { defineStore } from "pinia"
import { ref } from "vue"
import { AuthService } from "@/services/api/auth"
import { type User } from "@/types/user"
import { UserService } from "@/services/api/user"

export const useAuthStore = defineStore("auth", () => {
    const isAuthenticated = ref(false)
    const user = ref<User | null>(null)

    async function checkAuthStatus() {
        try {
            const { isValid } = await AuthService.verifyLogin()
            isAuthenticated.value = isValid
            // if the token has expired, remove the user's profile data
            if (!isValid) user.value = null
        } catch (error) {
            console.error("Authentication check failed:", error)
        }
    }

    async function getUserProfile() {
        try {
            user.value = await UserService.getUserProfile()
            isAuthenticated.value = true
        } catch (error) {
            console.error("Failed to get user profile:", error)
        }
    }

    async function logout() {
        try {
            await AuthService.logout()
            isAuthenticated.value = false
            user.value = null
        } catch (error) {
            console.error("Authentication logout failed:", error)
        }
    }

    return { isAuthenticated, user, checkAuthStatus, getUserProfile, logout }
})
