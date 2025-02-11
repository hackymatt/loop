import { PAYMENT_SERVER } from "src/config-global";

// ----------------------------------------------------------------------

export const paths = {
  // main
  root: "/",
  courses: "/courses",
  course: `/course`,
  teachers: "/teachers",
  teacher: "/teacher",
  posts: "/posts",
  post: "/post",
  about: "/about",
  contact: "/contact",
  newsletter: { subscribe: "/newsletter", unsubscribe: "/newsletter-unsubscribe" },
  cart: "/cart",
  checkout: "/checkout",
  order: {
    status: "/order-status",
    completed: "/order-completed",
    "not-completed": "/order-not-completed",
  },
  wishlist: "/wishlist",
  support: "/support",
  privacyPolicy: "/privacy-policy",
  termsAndConditions: "/terms-and-conditions",
  certificate: "/certificate",
  account: {
    root: "/account",
    personal: "/account/personal",
    manage: "/account/manage",
    messages: "/account/messages",
    admin: {
      courses: {
        list: "/account/admin/courses/list",
        topics: "/account/admin/courses/topics",
        candidates: "/account/admin/courses/candidates",
      },
      modules: {
        list: "/account/admin/modules/list",
      },
      lessons: {
        list: "/account/admin/lessons/list",
        priceHistory: "/account/admin/lessons/price-history",
        technologies: "/account/admin/lessons/technologies",
      },
      services: {
        list: "/account/admin/services/list",
      },
      posts: {
        list: "/account/admin/posts/list",
        categories: "/account/admin/posts/categories",
      },
      purchases: {
        lessons: {
          list: "/account/admin/purchases/list",
          payments: "/account/admin/purchases/payments",
        },
        services: {
          list: "/account/admin/purchases/list",
          payments: "/account/admin/purchases/payments",
        },
      },
      tags: "/account/admin/tags",
      users: {
        list: "/account/admin/users/list",
        financeHistory: "/account/admin/users/finance-history",
      },
      coupons: {
        list: "/account/admin/coupons/list",
        usage: "/account/admin/coupons/usage",
      },
      earnings: {
        company: "/account/admin/earnings/company",
        teachers: "/account/admin/earnings/teachers",
      },
      newsletter: "/account/admin/newsletter",
    },
    teacher: {
      profile: "/account/teacher/profile",
      finance: "/account/teacher/finance",
      teaching: "/account/teacher/teaching",
      earnings: "/account/teacher/earnings",
      reviews: "/account/teacher/reviews",
      calendar: "/account/teacher/calendar",
    },
    lessons: "/account/lessons",
    reviews: "/account/reviews",
    certificates: "/account/certificates",
  },
  login: "/login",
  register: "/register",
  forgotPassword: "/forgot-password",
  verify: "/verify",
  tests: {
    predisposition: "/tests/predisposition",
  },
  payment: {
    privacyPolicy: "https://www.przelewy24.pl/obowiazek-informacyjny-platnik",
    termsAndConditions: "https://www.przelewy24.pl/regulamin",
    url: `${PAYMENT_SERVER}/trnRequest`,
  },
};
