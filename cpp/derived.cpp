#include <bits/stdc++.h>
// like java List<? extends Integer>

struct A1 {
    virtual void a1() = 0;
};

struct A2 {
    virtual void a2() = 0;
};

struct A : public A1, A2 {
    void a1() {}
    void a2() {}
};

template <typename T>
struct B1 {
    virtual T b1() = 0;
};

template <typename T>
struct B2 {
    virtual T b2() = 0;
};

template <typename T>
struct B : public B1<T>, B2<T> {
    T b1() {}
    T b2() {}
};

template <typename T, typename = std::enable_if_t<std::is_base_of<A1, T>::value>>
struct C1 {
    virtual B1<T*>* c() = 0;
};

template <typename T, typename = std::enable_if_t<std::is_base_of<A2, T>::value>>
struct C2 {
    virtual B2<T*>* c() = 0;
};

struct C : public C1<A>, C2<A> {
    B<A*>* c() {}
};
