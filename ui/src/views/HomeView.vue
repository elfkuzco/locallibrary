<script setup lang="ts">
import FeaturedBooksComponent from "@/components/FeaturedBooksComponent.vue"
import { Icon } from "@iconify/vue"

const featuredBooks = [
    {
        title: "The Great Gatsby",
        author: "F. Scott Fitzgerald",
        image: {
            small: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
            medium: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800",
            large: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=1200",
            alt: "The Great Gatsby Book Cover",
        },
    },
    {
        title: "1984",
        author: "George Orwell",
        image: {
            small: "https://images.unsplash.com/photo-1495640388908-05b081ba96fb?w=400",
            medium: "https://images.unsplash.com/photo-1495640388908-05b081ba96fb?w=800",
            large: "https://images.unsplash.com/photo-1495640388908-05b081ba96fb?w=1200",
            alt: "1984 Book Cover",
        },
    },
    {
        title: "Pride and Prejudice",
        author: "Jane Austen",
        image: {
            small: "https://images.unsplash.com/photo-1603162525937-76c50da09c57?w=400",
            medium: "https://images.unsplash.com/photo-1603162525937-76c50da09c57?w=800",
            large: "https://images.unsplash.com/photo-1603162525937-76c50da09c57?w=1200",
            alt: "Pride and Prejudice Book Cover",
        },
    },
]

const statistics = [
    { number: "50K+", label: "Books Available" },
    { number: "10K+", label: "Active Members" },
    { number: "1000+", label: "Monthly Events" },
    { number: "24/7", label: "Digital Access" },
]

const initiativeImages = {
    literacy: {
        small: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400",
        medium: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800",
        alt: "Adult Literacy Program",
    },
    stem: {
        small: "https://images.unsplash.com/photo-1588072432836-e10032774350?w=400",
        medium: "https://images.unsplash.com/photo-1588072432836-e10032774350?w=800",
        alt: "Youth STEM Workshop",
    },
    senior: {
        small: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400",
        medium: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800",
        alt: "Senior Tech Support",
    },
}

const services = [
    {
        title: "Books & Media",
        icon: "material-symbols:library-books",
        items: ["Physical Books", "E-Books & Audiobooks", "Magazines & Journals"],
    },
    {
        title: "Digital Resources",
        icon: "material-symbols:computer",
        items: ["Online Databases", "Learning Platforms", "Research Tools"],
    },
    {
        title: "Community Programs",
        icon: "material-symbols:groups",
        items: ["Book Clubs", "Children's Events", "Workshops"],
    },
    {
        title: "Study Spaces",
        icon: "material-symbols:meeting-room",
        items: ["Private Rooms", "Group Areas", "Quiet Zones"],
    },
]

const events = [
    {
        date: "2024-03-20",
        title: "Author Meet & Greet",
        time: "6:00 PM",
        location: "Main Hall",
    },
    // ...more events
]
</script>

<template>
    <div>
        <!-- Hero Section -->
        <section class="relative h-[60vh] mb-12">
            <div class="absolute inset-0">
                <picture>
                    <source
                        srcset="https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=2000"
                        media="(min-width: 1280px)"
                    />
                    <source
                        srcset="https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1200"
                        media="(min-width: 768px)"
                    />
                    <img
                        src="https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800"
                        class="w-full h-full object-cover"
                        alt="Library interior"
                        loading="eager"
                    />
                </picture>
            </div>
            <div class="relative max-w-7xl mx-auto px-4 h-full flex items-center">
                <div class="text-white max-w-2xl">
                    <h1 class="text-5xl font-bold mb-4">Discover, Learn, Grow</h1>
                    <p class="text-xl mb-8">Your gateway to knowledge and community connection</p>
                    <button
                        class="bg-white text-blue-900 px-8 py-3 rounded-full hover:bg-blue-50 transition"
                    >
                        Explore Collection
                    </button>
                </div>
            </div>
        </section>

        <!-- Featured Books -->
        <FeaturedBooksComponent :featuredBooks="featuredBooks" />

        <!-- Impact Statistics -->
        <section class="bg-blue-50 py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
                    <div v-for="stat in statistics" :key="stat.label" class="text-center">
                        <div class="text-4xl font-bold text-blue-600 mb-2">{{ stat.number }}</div>
                        <div class="text-gray-600">{{ stat.label }}</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Community Initiatives -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-8">Community Initiatives</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <picture>
                        <source
                            :srcset="initiativeImages.literacy.medium"
                            media="(min-width: 768px)"
                        />
                        <img
                            :src="initiativeImages.literacy.small"
                            :alt="initiativeImages.literacy.alt"
                            class="w-full h-48 object-cover"
                            loading="lazy"
                        />
                    </picture>
                    <div class="p-6">
                        <h3 class="text-xl font-bold mb-2">Adult Literacy Program</h3>
                        <p class="text-gray-600">
                            Free literacy classes for adults looking to improve their reading
                            skills.
                        </p>
                    </div>
                </div>
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <picture>
                        <source :srcset="initiativeImages.stem.medium" media="(min-width: 768px)" />
                        <img
                            :src="initiativeImages.stem.small"
                            :alt="initiativeImages.stem.alt"
                            class="w-full h-48 object-cover"
                            loading="lazy"
                        />
                    </picture>
                    <div class="p-6">
                        <h3 class="text-xl font-bold mb-2">Youth STEM Workshops</h3>
                        <p class="text-gray-600">
                            Engaging science and technology programs for young minds.
                        </p>
                    </div>
                </div>
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                    <picture>
                        <source
                            :srcset="initiativeImages.senior.medium"
                            media="(min-width: 768px)"
                        />
                        <img
                            :src="initiativeImages.senior.small"
                            :alt="initiativeImages.senior.alt"
                            class="w-full h-48 object-cover"
                            loading="lazy"
                        />
                    </picture>
                    <div class="p-6">
                        <h3 class="text-xl font-bold mb-2">Senior Tech Support</h3>
                        <p class="text-gray-600">
                            Helping seniors navigate the digital world with confidence.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Mission Section -->
        <section class="bg-gradient-to-br from-indigo-50 to-emerald-50 py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4">
                <div class="max-w-3xl mx-auto text-center">
                    <Icon
                        icon="material-symbols:auto-stories-rounded"
                        class="text-indigo-600 text-5xl mb-6"
                    />
                    <h2 class="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
                    <p class="text-lg text-gray-600 leading-relaxed">
                        At LocalLibrary, we create a vibrant space where knowledge meets community.
                        Our mission is to inspire lifelong learning, foster creativity, and build
                        meaningful connections through accessible resources and innovative programs.
                    </p>
                </div>
            </div>
        </section>

        <!-- Services Grid -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">
                Everything You Need to Succeed
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div
                    v-for="service in services"
                    :key="service.title"
                    class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                    <Icon :icon="service.icon" class="text-4xl text-indigo-600 mb-4" />
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">{{ service.title }}</h3>
                    <ul class="space-y-3">
                        <li
                            v-for="item in service.items"
                            :key="item"
                            class="flex items-center text-gray-600"
                        >
                            <Icon
                                icon="material-symbols:check-circle"
                                class="text-emerald-500 mr-2"
                            />
                            {{ item }}
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- Events Calendar -->
        <section class="bg-gray-50 py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4">
                <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">Upcoming Events</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div
                        v-for="event in events"
                        :key="event.title"
                        class="bg-white rounded-xl shadow-lg overflow-hidden group hover:shadow-xl transition-all duration-300"
                    >
                        <div
                            class="bg-indigo-600 text-white p-4 group-hover:bg-indigo-700 transition-colors"
                        >
                            <div class="text-lg font-semibold">
                                {{
                                    new Date(event.date).toLocaleDateString("en-US", {
                                        month: "short",
                                        day: "numeric",
                                    })
                                }}
                            </div>
                        </div>
                        <div class="p-6">
                            <h3 class="text-xl font-semibold text-gray-900 mb-2">
                                {{ event.title }}
                            </h3>
                            <div class="flex items-center text-gray-600 mb-2">
                                <Icon icon="material-symbols:schedule" class="mr-2" />
                                {{ event.time }}
                            </div>
                            <div class="flex items-center text-gray-600">
                                <Icon icon="material-symbols:location-on" class="mr-2" />
                                {{ event.location }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Membership Benefits -->
        <section class="max-w-7xl mx-auto px-4 mb-16">
            <div
                class="bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-2xl p-8 md:p-12 text-white"
            >
                <div class="max-w-3xl">
                    <h2 class="text-3xl font-bold mb-6">Become a Member Today</h2>
                    <p class="text-lg mb-8 text-indigo-100">
                        Join our community and get access to exclusive benefits, events, and
                        resources.
                    </p>
                    <button
                        class="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-indigo-50 transition-colors"
                    >
                        Sign Up Now
                    </button>
                </div>
            </div>
        </section>

        <!-- Newsletter Signup -->
        <section class="bg-blue-900 text-white py-16 mb-16">
            <div class="max-w-7xl mx-auto px-4 text-center">
                <h2 class="text-3xl font-bold mb-4">Stay Connected</h2>
                <p class="mb-8">
                    Subscribe to our newsletter for updates on events and new arrivals
                </p>
                <form class="max-w-md mx-auto flex gap-4">
                    <input
                        type="email"
                        placeholder="Enter your email"
                        class="flex-1 px-4 py-2 rounded-lg text-gray-900"
                    />
                    <button
                        class="bg-white text-blue-900 px-6 py-2 rounded-lg hover:bg-blue-50 transition"
                    >
                        Subscribe
                    </button>
                </form>
            </div>
        </section>
    </div>
</template>
