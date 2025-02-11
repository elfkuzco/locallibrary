<template>
    <main>
        <!-- Hero Section -->
        <section class="relative h-[40vh] mb-16">
            <div class="absolute inset-0 bg-gradient-to-r from-indigo-900/90 to-indigo-800/90">
                <img
                    src="https://images.unsplash.com/photo-1568667256549-094345857637?w=1200"
                    alt="Library interior"
                    class="w-full h-full object-cover mix-blend-overlay"
                />
            </div>
            <div class="relative max-w-7xl mx-auto px-4 h-full flex items-center">
                <div class="text-white max-w-2xl">
                    <h1 class="text-4xl font-bold mb-4">Our Story</h1>
                    <p class="text-xl text-gray-200">
                        Building community through knowledge since 1998
                    </p>
                </div>
            </div>
        </section>

        <!-- Story Section -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <div class="bg-white rounded-2xl shadow-lg p-8 md:p-12">
                <div class="max-w-3xl mx-auto">
                    <h2 class="text-3xl font-bold text-gray-900 mb-6">A Journey of Growth</h2>
                    <p class="text-gray-600 leading-relaxed mb-6">
                        Founded in 1998, LocalLibrary has been a cornerstone of our community for
                        decades. From humble beginnings as a small collection of books, we have
                        grown into a vibrant hub of knowledge and culture, serving thousands of
                        patrons every year.
                    </p>
                    <p class="text-gray-600 leading-relaxed">
                        Our library continues to adapt and evolve, embracing the digital age while
                        staying true to our core mission of fostering learning, creativity, and
                        connection.
                    </p>
                </div>
            </div>
        </section>

        <!-- Mission Section -->
        <section class="bg-gradient-to-br from-indigo-50 to-emerald-50 py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4">
                <div class="max-w-3xl mx-auto text-center">
                    <Icon icon="material-symbols:mission" class="text-indigo-600 text-5xl mb-6" />
                    <h2 class="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
                    <p class="text-lg text-gray-600 leading-relaxed">
                        At LocalLibrary, we are dedicated to empowering individuals, enriching
                        lives, and strengthening our community through accessible resources,
                        inclusive programs, and a welcoming environment for all.
                    </p>
                </div>
            </div>
        </section>

        <!-- Values Grid -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Our Values</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div
                    v-for="value in values"
                    :key="value.title"
                    class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                    <Icon :icon="value.icon" class="text-4xl text-indigo-600 mb-4" />
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ value.title }}</h3>
                    <p class="text-gray-600">{{ value.description }}</p>
                </div>
            </div>
        </section>

        <!-- Team Stats -->
        <section class="bg-gray-50 py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4">
                <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Our Impact</h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                    <div v-for="stat in stats" :key="stat.label" class="text-center">
                        <div class="text-4xl font-bold text-indigo-600 mb-2">{{ stat.number }}</div>
                        <div class="text-gray-600">{{ stat.label }}</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Join Section -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <div
                class="bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-2xl p-8 md:p-12 text-white"
            >
                <div class="max-w-3xl">
                    <h2 class="text-3xl font-bold mb-6">Join Our Community</h2>
                    <p class="text-lg mb-8 text-indigo-100">
                        Whether you're interested in volunteering, donating, or simply sharing your
                        ideas, we'd love to hear from you. Together, we can continue to make
                        LocalLibrary a vital part of our community.
                    </p>
                    <RouterLink
                        to="/contact"
                        class="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-indigo-50 transition-colors"
                    >
                        Get Involved
                    </RouterLink>
                </div>
            </div>
        </section>
    </main>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue"

const values = [
    {
        icon: "material-symbols:diversity-3",
        title: "Inclusivity",
        description: "We welcome everyone, respecting diversity and promoting equity.",
    },
    {
        icon: "material-symbols:lightbulb",
        title: "Innovation",
        description: "We embrace change and continuously improve to meet evolving needs.",
    },
    {
        icon: "material-symbols:people-outline",
        title: "Community",
        description: "We build connections and foster a sense of belonging.",
    },
    {
        icon: "material-symbols:school",
        title: "Knowledge",
        description: "We champion the pursuit of learning and the sharing of ideas.",
    },
]

const stats = [
    { number: "25+", label: "Years of Service" },
    { number: "50+", label: "Team Members" },
    { number: "100K+", label: "Community Members" },
    { number: "500+", label: "Annual Programs" },
]
</script>
