import { notFound } from "next/navigation";

import { siteConfig } from "@/config/site";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface ProjectDetailPageProps {
  params: { slug: string };
}

export default function ProjectDetailPage({ params }: ProjectDetailPageProps) {
  const project = siteConfig.projects.find((item) => item.slug === params.slug);

  if (!project) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto w-full max-w-5xl px-6 py-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-emerald-600">
              {project.sector} · {project.stage}
            </p>
            <h1 className="text-3xl font-semibold text-slate-900 md:text-4xl">
              {project.name}
            </h1>
            <p className="text-sm text-slate-500">{project.location}</p>
          </div>
          <Button>Request Investment Memo</Button>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[2fr,1fr]">
          <Card>
            <CardHeader>
              <CardTitle>Project Overview</CardTitle>
              <p className="text-sm text-slate-500">{project.summary}</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-4 md:grid-cols-3">
                <div>
                  <p className="text-xs uppercase text-slate-500">Funding Target</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.fundingTarget}
                  </p>
                </div>
                <div>
                  <p className="text-xs uppercase text-slate-500">Equity Offer</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.equityOffer}
                  </p>
                </div>
                <div>
                  <p className="text-xs uppercase text-slate-500">Timeline</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.timeline}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-xs uppercase text-slate-500">Impact Focus</p>
                <div className="mt-2 rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-700">
                  {project.impact}
                </div>
              </div>
              <div className="grid gap-4 md:grid-cols-3">
                <div>
                  <p className="text-xs uppercase text-slate-500">Projected IRR</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.metrics.irr}
                  </p>
                </div>
                <div>
                  <p className="text-xs uppercase text-slate-500">Payback</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.metrics.payback}
                  </p>
                </div>
                <div>
                  <p className="text-xs uppercase text-slate-500">Jobs Created</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {project.metrics.jobs}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-xs uppercase text-slate-500">Impact Delivery</p>
                <div className="mt-3 space-y-3">
                  <div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">ESG readiness</span>
                      <span className="font-medium text-slate-900">82%</span>
                    </div>
                    <Progress value={82} />
                  </div>
                  <div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Community adoption</span>
                      <span className="font-medium text-slate-900">68%</span>
                    </div>
                    <Progress value={68} />
                  </div>
                  <div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Carbon reduction</span>
                      <span className="font-medium text-slate-900">74%</span>
                    </div>
                    <Progress value={74} />
                  </div>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <Badge key={tag} variant="outline">
                    {tag}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Project Sponsor</CardTitle>
                <p className="text-sm text-slate-500">
                  AFCEN-accredited project owner with audited financials.
                </p>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-slate-600">
                <p>Lead organization: GreenRidge Capital</p>
                <p>ESG rating: AA-</p>
                <p>Last diligence: June 2024</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Next Steps</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-slate-600">
                <p>1. Request full data room access.</p>
                <p>2. Schedule diligence call with sponsor.</p>
                <p>3. Draft term sheet with AFCEN guidance.</p>
              </CardContent>
            </Card>
            <Button className="w-full">Schedule Due Diligence Call</Button>
          </div>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
