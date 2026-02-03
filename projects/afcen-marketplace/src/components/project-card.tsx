import Link from "next/link";

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ProjectCardProps {
  project: {
    slug: string;
    name: string;
    location: string;
    sector: string;
    stage: string;
    summary: string;
    fundingTarget: string;
    equityOffer: string;
    impact: string;
    tags: string[];
  };
}

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Card className="flex h-full flex-col">
      <CardHeader className="space-y-3">
        <div className="flex items-center justify-between">
          <Badge variant="secondary">{project.sector}</Badge>
          <span className="text-xs font-semibold uppercase tracking-wide text-emerald-600">
            {project.stage}
          </span>
        </div>
        <CardTitle>{project.name}</CardTitle>
        <p className="text-sm text-slate-600">{project.location}</p>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-slate-600">{project.summary}</p>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-xs uppercase text-slate-500">Target</p>
            <p className="font-semibold text-slate-900">
              {project.fundingTarget}
            </p>
          </div>
          <div>
            <p className="text-xs uppercase text-slate-500">Offer</p>
            <p className="font-semibold text-slate-900">{project.equityOffer}</p>
          </div>
        </div>
        <div className="rounded-lg bg-emerald-50 px-3 py-2 text-xs text-emerald-700">
          {project.impact}
        </div>
        <div className="flex flex-wrap gap-2">
          {project.tags.map((tag) => (
            <Badge key={tag} variant="outline">
              {tag}
            </Badge>
          ))}
        </div>
      </CardContent>
      <CardFooter className="mt-auto flex items-center justify-between">
        <Link
          href={`/projects/${project.slug}`}
          className={cn(buttonVariants({ variant: "outline", size: "sm" }))}
        >
          View Detail
        </Link>
        <Button size="sm">Request Intro</Button>
      </CardFooter>
    </Card>
  );
}
