<script setup lang="ts">
import type { NavigationLink } from "@/types/link"

defineProps<{
    quickLinks: NavigationLink[]
    services: NavigationLink[]
    legal: NavigationLink[]
}>()
</script>

<template>
    <div class="bg-gray-900 text-white pt-16 pb-8 max-w-7xl mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 mb-12">
            <!-- About -->
            <div>
                <h3 class="text-xl font-bold mb-4">LocalLibrary</h3>
                <p class="text-gray-400 mb-4">
                    Empowering our community through knowledge, innovation, and connection since
                    1985.
                </p>
                <div class="flex space-x-4">
                    <a href="#" class="text-gray-400 hover:text-white transition-colors">
                        <Icon icon="mdi:facebook" class="text-2xl" />
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition-colors">
                        <Icon icon="mdi:twitter" class="text-2xl" />
                    </a>
                    <a href="#" class="text-gray-400 hover:text-white transition-colors">
                        <Icon icon="mdi:instagram" class="text-2xl" />
                    </a>
                </div>
            </div>

            <!-- Quick Links -->
            <div>
                <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
                <ul class="space-y-2">
                    <li v-for="link in quickLinks" :key="link.name">
                        <a
                            :href="link.path"
                            class="text-gray-400 hover:text-white transition-colors"
                        >
                            {{ link.name }}
                        </a>
                    </li>
                </ul>
            </div>

            <!-- Services -->
            <div>
                <h3 class="text-lg font-semibold mb-4">Services</h3>
                <ul class="space-y-2">
                    <li v-for="link in services" :key="link.name">
                        <a
                            :href="link.path"
                            class="text-gray-400 hover:text-white transition-colors"
                        >
                            {{ link.name }}
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <!-- Bottom Footer -->
        <div class="pt-8 border-t border-gray-800 text-center text-gray-400 text-sm">
            <div class="flex flex-wrap justify-center gap-4 mb-4">
                <a
                    v-for="link in legal"
                    :key="link.name"
                    :href="link.path"
                    class="hover:text-white transition-colors"
                >
                    {{ link.name }}
                </a>
            </div>
            <p>&copy; {{ new Date().getFullYear() }} LocalLibrary. All rights reserved.</p>
        </div>
    </div>
</template>
