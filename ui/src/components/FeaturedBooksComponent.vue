<script setup lang="ts">
import type { FeaturedBook } from "@/types/book"

defineProps<{ featuredBooks: FeaturedBook[] }>()
</script>

<template>
    <!-- Featured Books -->
    <section class="max-w-7xl mx-auto px-4 mb-16">
        <h2 class="text-3xl font-bold text-gray-900 mb-8">Featured Books</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
                v-for="book in featuredBooks"
                :key="book.title"
                class="group relative overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition"
            >
                <picture>
                    <source :srcset="book.image.large" media="(min-width: 1024px)" />
                    <source :srcset="book.image.medium" media="(min-width: 640px)" />
                    <img
                        :src="book.image.small"
                        :alt="book.image.alt"
                        class="w-full h-64 object-cover"
                        loading="lazy"
                    />
                </picture>
                <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 p-4">
                    <h3 class="text-white font-semibold">{{ book.title }}</h3>
                    <p class="text-gray-300 text-sm">{{ book.author }}</p>
                </div>
            </div>
        </div>
    </section>
</template>
