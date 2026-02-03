import Link from "next/link";

import { siteConfig } from "@/config/site";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { ProjectCard } from "@/components/project-card";
import { FilterSidebar } from "@/components/filter-sidebar";
import { MapPanel } from "@/components/map-panel";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto w-full max-w-6xl px-6 py-10">
        <section className="grid gap-8 lg:grid-cols-[1.1fr,0.9fr]">
          <div className="space-y-6">
            <p className="text-sm font-semibold uppercase tracking-wide text-emerald-600">
              {siteConfig.name}
            </p>
            <h1 className="text-4xl font-semibold leading-tight text-slate-900 md:text-5xl">
              {siteConfig.hero.title}
            </h1>
            <p className="text-lg text-slate-600">{siteConfig.hero.subtitle}</p>
            <div className="flex flex-wrap gap-3">
              <Button>{siteConfig.hero.ctaPrimary}</Button>
              <Button variant="outline">{siteConfig.hero.ctaSecondary}</Button>
            </div>
          </div>
          <Card className="flex flex-col gap-6 bg-gradient-to-br from-white via-white to-emerald-50 p-8">
            <div className="space-y-2">
              <h2 className="text-xl font-semibold text-slate-900">
                Marketplace Highlights
              </h2>
              <p className="text-sm text-slate-600">
                Stay informed with real-time signals from AFCEN's pipeline.
              </p>
            </div>
            <div className="grid gap-4">
              {siteConfig.stats.map((stat) => (
                <div key={stat.label} className="flex items-center justify-between">
                  <p className="text-sm text-slate-500">{stat.label}</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {stat.value}
                  </p>
                </div>
              ))}
            </div>
            <Link
              href="/dashboard"
              className="text-sm font-semibold text-emerald-600 hover:text-emerald-700"
            >
              View investor analytics →
            </Link>
          </Card>
        </section>

        <section className="mt-12 grid gap-8 lg:grid-cols-[280px,1fr]">
          <FilterSidebar />
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-slate-900">
                  Featured Projects
                </h2>
                <p className="text-sm text-slate-500">
                  Curated, investment-ready opportunities across Kenya.
                </p>
              </div>
              <Button variant="ghost">View all</Button>
            </div>
            <div className="grid gap-6 md:grid-cols-2">
              {siteConfig.projects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
            <MapPanel />
          </div>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
