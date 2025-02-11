<script setup lang="ts">
import { ref } from "vue"
import { Icon } from "@iconify/vue"
import type { User } from "@/types/user"

import type { NavigationLink } from "@/types/link"

const isMobileMenuOpen = ref(false)
const isUserMenuOpen = ref(false)

defineProps<{ navigationLinks: NavigationLink[]; user: User | null; isAuthenticated: boolean }>()

const emit = defineEmits<{
    logout: []
}>()
</script>

<template>
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between h-16">
                <!-- Logo and Primary Navigation -->
                <div class="flex">
                    <!-- Logo -->
                    <div class="flex-shrink-0 flex items-center">
                        <RouterLink to="/" class="flex items-center space-x-2">
                            <Icon
                                icon="material-symbols:library-books"
                                class="h-8 w-8 text-indigo-600"
                            />
                            <span class="text-xl font-bold text-gray-900">LocalLibrary</span>
                        </RouterLink>
                    </div>

                    <!-- Desktop Navigation -->
                    <div class="hidden lg:ml-6 lg:flex lg:space-x-4">
                        <RouterLink
                            v-for="link in navigationLinks"
                            :key="link.name"
                            :to="link.path"
                            class="inline-flex items-center px-3 py-2 text-gray-600 hover:text-indigo-600 rounded-md text-sm font-medium"
                            active-class="text-indigo-600"
                        >
                            {{ link.name }}
                        </RouterLink>
                    </div>
                </div>

                <!-- Search and Auth -->
                <div class="flex items-center">
                    <!-- Search Bar -->
                    <div class="hidden lg:flex items-center px-2">
                        <div class="relative">
                            <input
                                type="text"
                                placeholder="Search catalog..."
                                class="w-72 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
                            />
                            <Icon
                                icon="material-symbols:search"
                                class="absolute left-3 top-2.5 text-gray-400"
                            />
                        </div>
                    </div>

                    <!-- Auth Buttons -->
                    <div class="flex items-center ml-4 space-x-4">
                        <template v-if="!isAuthenticated">
                            <RouterLink
                                to="/register"
                                class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
                            >
                                Sign in
                            </RouterLink>
                        </template>
                        <template v-else>
                            <!-- User Menu Dropdown -->
                            <div class="relative">
                                <button
                                    @click="isUserMenuOpen = !isUserMenuOpen"
                                    class="flex items-center space-x-2 text-gray-600 hover:text-indigo-600"
                                >
                                    <Icon icon="material-symbols:account-circle" class="w-8 h-8" />
                                    <span class="text-sm font-medium">{{ user?.firstName }}</span>
                                </button>
                                <!-- Dropdown Menu -->
                                <div
                                    v-show="isUserMenuOpen"
                                    class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 ring-1 ring-black ring-opacity-5"
                                    style="transform-origin: top right"
                                >
                                    <RouterLink
                                        to="/account"
                                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                        @click="isUserMenuOpen = false"
                                    >
                                        My Account
                                    </RouterLink>
                                    <RouterLink
                                        to="/loans"
                                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                        @click="isUserMenuOpen = false"
                                    >
                                        My Loans
                                    </RouterLink>
                                    <button
                                        @click="
                                            () => {
                                                emit('logout')
                                                isUserMenuOpen = false
                                            }
                                        "
                                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    >
                                        Sign out
                                    </button>
                                </div>
                            </div>
                        </template>
                    </div>

                    <!-- Mobile menu button -->
                    <button
                        @click="isMobileMenuOpen = !isMobileMenuOpen"
                        class="lg:hidden ml-2 p-2 rounded-md text-gray-600 hover:text-indigo-600"
                    >
                        <Icon
                            :icon="
                                isMobileMenuOpen
                                    ? 'material-symbols:close'
                                    : 'material-symbols:menu'
                            "
                            class="h-6 w-6"
                        />
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile menu -->
        <div v-show="isMobileMenuOpen" class="lg:hidden">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <RouterLink
                    v-for="link in navigationLinks"
                    :key="link.name"
                    :to="link.path"
                    class="block px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-indigo-600"
                    active-class="text-indigo-600"
                    @click="isMobileMenuOpen = false"
                >
                    {{ link.name }}
                </RouterLink>
            </div>
            <!-- Mobile Search -->
            <div class="px-2 py-3 border-t border-gray-200">
                <div class="relative">
                    <input
                        type="text"
                        placeholder="Search catalog..."
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <Icon
                        icon="material-symbols:search"
                        class="absolute left-3 top-2.5 text-gray-400"
                    />
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.absolute {
    position: absolute;
}

/* Add transition for smooth appearance */
.absolute {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}
</style>
