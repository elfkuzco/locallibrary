<script setup lang="ts">
import { RouterView } from "vue-router"
import FooterComponent from "@/components/FooterComponent.vue"
import NavbarComponent from "@/components/NavbarComponent.vue"
import { useAuthStore } from "@/stores/auth"
import { onMounted } from "vue"

const authStore = useAuthStore()

const { logout } = authStore

onMounted(async () => {
    // check if the user is authenticated.
    await authStore.getUserProfile()
})

const navigationLinks = [
    { name: "Home", path: "/" },
    { name: "Catalog", path: "/catalog" },
    {
        name: "Services",
        path: "/services",
        dropdown: [
            { name: "Book a Room", path: "/services/rooms" },
            { name: "Print & Copy", path: "/services/print" },
            { name: "Research Help", path: "/services/research" },
        ],
    },
    { name: "Events", path: "/events" },
    { name: "About", path: "/about" },
]

const footerLinks = {
    quickLinks: [
        { name: "Search Catalog", path: "/catalog" },
        { name: "My Account", path: "/account" },
        { name: "Events Calendar", path: "/events" },
        { name: "Research Resources", path: "/resources" },
    ],
    services: [
        { name: "Book Recommendations", path: "/recommendations" },
        { name: "Interlibrary Loan", path: "/loan" },
        { name: "Study Room Booking", path: "/rooms" },
        { name: "Print Services", path: "/services" },
    ],
    legal: [
        { name: "Privacy Policy", path: "/privacy" },
        { name: "Terms of Use", path: "/terms" },
        { name: "Accessibility", path: "/accessibility" },
    ],
}
</script>

<template>
    <header>
        <NavbarComponent
            :navigationLinks="navigationLinks"
            :isAuthenticated="authStore.isAuthenticated"
            :user="authStore.user"
            @logout="async () => await logout()"
        />
    </header>

    <main>
        <RouterView />
    </main>

    <footer>
        <FooterComponent
            :quickLinks="footerLinks.quickLinks"
            :legal="footerLinks.legal"
            :services="footerLinks.services"
        />
    </footer>
</template>
