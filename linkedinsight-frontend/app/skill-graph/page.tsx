'use client';

/**
 * Skill Graph Explorer Page
 * 
 * Explore skill relationships, prerequisites, and learning paths
 */

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Search, 
  Network, 
  ArrowRight, 
  BookOpen, 
  Loader2,
  CheckCircle2
} from 'lucide-react';
import { getRelated, getPrereqs, getLearningPath, getAllSkills } from '@/app/api/skills';
import type { RelatedSkillsResponse, PrerequisitesResponse, LearningPathResponse } from '@/app/api/types';

type ViewMode = 'prereqs' | 'related' | 'path' | null;

export default function SkillGraphPage() {
  const [skill, setSkill] = useState('');
  const [viewMode, setViewMode] = useState<ViewMode>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Fetch all available skills for suggestions
  const { data: allSkillsData } = useQuery({
    queryKey: ['all-skills'],
    queryFn: getAllSkills,
  });

  // Prerequisites query
  const { 
    data: prereqsData, 
    isLoading: prereqsLoading,
    error: prereqsError 
  } = useQuery({
    queryKey: ['skill-prereqs', skill],
    queryFn: () => getPrereqs(skill),
    enabled: viewMode === 'prereqs' && skill.trim() !== '',
  });

  // Related skills query
  const { 
    data: relatedData, 
    isLoading: relatedLoading,
    error: relatedError 
  } = useQuery({
    queryKey: ['skill-related', skill],
    queryFn: () => getRelated(skill),
    enabled: viewMode === 'related' && skill.trim() !== '',
  });

  // Learning path query
  const { 
    data: pathData, 
    isLoading: pathLoading,
    error: pathError 
  } = useQuery({
    queryKey: ['skill-path', skill],
    queryFn: () => getLearningPath(skill),
    enabled: viewMode === 'path' && skill.trim() !== '',
  });

  const handleView = (mode: ViewMode) => {
    if (skill.trim()) {
      setViewMode(mode);
    }
  };

  return (
    <div className="p-6 md:p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Skill Graph Explorer</h1>
        <p className="text-gray-600">Explore skill relationships, prerequisites, and learning paths</p>
      </div>

      {/* Search Section */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Search for a Skill</CardTitle>
          <CardDescription>
            Enter a skill name to explore its relationships in the skills graph
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Input
                placeholder="e.g., Python, Machine Learning, Data Science..."
                value={skill}
                onChange={(e) => {
                  setSkill(e.target.value);
                  setShowSuggestions(e.target.value.length > 0);
                }}
                onFocus={() => setShowSuggestions(skill.length > 0 && allSkillsData?.skills.length > 0)}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && skill.trim()) {
                    setViewMode('related');
                    setShowSuggestions(false);
                  }
                }}
                className="text-base"
              />
              {/* Skill Suggestions */}
              {showSuggestions && allSkillsData && allSkillsData.skills.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-y-auto">
                  {allSkillsData.skills
                    .filter(s => s.toLowerCase().includes(skill.toLowerCase()))
                    .slice(0, 10)
                    .map((suggestedSkill) => (
                      <button
                        key={suggestedSkill}
                        type="button"
                        onClick={() => {
                          setSkill(suggestedSkill);
                          setShowSuggestions(false);
                        }}
                        className="w-full text-left px-4 py-2 hover:bg-[#0077B5]/10 hover:text-[#0077B5] transition-colors"
                      >
                        {suggestedSkill}
                      </button>
                    ))}
                  {allSkillsData.skills.filter(s => s.toLowerCase().includes(skill.toLowerCase())).length === 0 && (
                    <div className="px-4 py-2 text-sm text-gray-500">
                      No matching skills found
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="flex gap-2">
              <Button
                onClick={() => handleView('prereqs')}
                disabled={!skill.trim()}
                variant="outline"
                className="border-[#0077B5] text-[#0077B5] hover:bg-[#0077B5] hover:text-white"
              >
                Prerequisites
              </Button>
              <Button
                onClick={() => handleView('related')}
                disabled={!skill.trim()}
                variant="outline"
                className="border-[#0077B5] text-[#0077B5] hover:bg-[#0077B5] hover:text-white"
              >
                Related Skills
              </Button>
              <Button
                onClick={() => handleView('path')}
                disabled={!skill.trim()}
                className="bg-[#0077B5] hover:bg-[#004182]"
              >
                Learning Path
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Prerequisites View */}
      {viewMode === 'prereqs' && (
        <Card>
          <CardHeader>
            <CardTitle>Prerequisites for "{skill}"</CardTitle>
            <CardDescription>Skills you need to learn before this one</CardDescription>
          </CardHeader>
          <CardContent>
            {prereqsLoading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-[#0077B5]" />
              </div>
            )}
            {prereqsError && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800 font-semibold mb-2">Error loading prerequisites</p>
                <p className="text-red-600 text-sm">
                  {prereqsError instanceof Error ? prereqsError.message : 'Failed to fetch prerequisites'}
                </p>
                {allSkillsData && allSkillsData.skills.length > 0 && (
                  <div className="mt-3">
                    <p className="text-red-700 text-sm mb-2">Available skills include:</p>
                    <div className="flex flex-wrap gap-2">
                      {allSkillsData.skills.slice(0, 10).map((s) => (
                        <Badge key={s} variant="outline" className="text-xs">
                          {s}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
            {prereqsData && (
              <div>
                {prereqsData.prerequisites.length === 0 ? (
                  <div className="text-center py-8 text-gray-600">
                    <CheckCircle2 className="h-12 w-12 text-green-500 mx-auto mb-4" />
                    <p className="text-lg font-medium">No prerequisites!</p>
                    <p>You can start learning "{skill}" directly.</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm text-gray-600 mb-4">
                      Found {prereqsData.count} prerequisite{prereqsData.count === 1 ? '' : 's'}
                    </p>
                    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                      {prereqsData.prerequisites.map((prereq) => (
                        <div
                          key={prereq}
                          className="p-4 rounded-lg border border-gray-200 bg-gray-50 hover:border-[#0077B5] transition-colors"
                        >
                          <div className="flex items-center gap-2">
                            <BookOpen className="h-4 w-4 text-[#0077B5]" />
                            <span className="font-medium text-gray-900">{prereq}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Related Skills View */}
      {viewMode === 'related' && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Prerequisites</CardTitle>
              <CardDescription>Skills needed before "{skill}"</CardDescription>
            </CardHeader>
            <CardContent>
              {relatedLoading && (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-[#0077B5]" />
                </div>
              )}
              {relatedError && (
                <div className="text-red-600 text-sm">
                  Error loading related skills
                </div>
              )}
              {relatedData && (
                <div className="space-y-2">
                  {relatedData.prerequisites.length === 0 ? (
                    <p className="text-sm text-gray-500">No prerequisites</p>
                  ) : (
                    relatedData.prerequisites.map((prereq) => (
                      <Badge key={prereq} variant="outline" className="mr-2 mb-2">
                        {prereq}
                      </Badge>
                    ))
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Successors</CardTitle>
              <CardDescription>Skills you can learn after "{skill}"</CardDescription>
            </CardHeader>
            <CardContent>
              {relatedLoading && (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-[#0077B5]" />
                </div>
              )}
              {relatedError && (
                <div className="text-red-600 text-sm">
                  Error loading related skills
                </div>
              )}
              {relatedData && (
                <div className="space-y-2">
                  {relatedData.successors.length === 0 ? (
                    <p className="text-sm text-gray-500">No successors yet</p>
                  ) : (
                    relatedData.successors.map((successor) => (
                      <Badge key={successor} variant="outline" className="mr-2 mb-2">
                        {successor}
                      </Badge>
                    ))
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Learning Path View */}
      {viewMode === 'path' && (
        <Card>
          <CardHeader>
            <CardTitle>Learning Path to "{skill}"</CardTitle>
            <CardDescription>{pathData?.message || 'Ordered list of skills to learn'}</CardDescription>
          </CardHeader>
          <CardContent>
            {pathLoading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-[#0077B5]" />
              </div>
            )}
            {pathError && (
              <div className="text-red-600">
                Error: {pathError instanceof Error ? pathError.message : 'Failed to generate learning path'}
              </div>
            )}
            {pathData && (
              <div>
                {pathData.learning_path.length === 0 ? (
                  <div className="text-center py-8 text-gray-600">
                    <p>No learning path found for "{skill}"</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-6">
                      <Network className="h-4 w-4" />
                      <span>Path length: {pathData.path_length} skill{pathData.path_length === 1 ? '' : 's'}</span>
                    </div>
                    <div className="space-y-3">
                      {pathData.learning_path.map((pathSkill, index) => (
                        <div
                          key={pathSkill}
                          className="flex items-center gap-4 p-4 rounded-lg border border-gray-200 bg-white hover:border-[#0077B5] hover:shadow-sm transition-all"
                        >
                          <div className="flex-shrink-0 h-8 w-8 rounded-full bg-[#0077B5] text-white flex items-center justify-center font-semibold">
                            {index + 1}
                          </div>
                          <div className="flex-1">
                            <p className="font-medium text-gray-900">{pathSkill}</p>
                            {index === pathData.learning_path.length - 1 && (
                              <Badge className="mt-1 bg-green-100 text-green-800">Target Skill</Badge>
                            )}
                          </div>
                          {index < pathData.learning_path.length - 1 && (
                            <ArrowRight className="h-5 w-5 text-gray-400" />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {!viewMode && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardContent className="pt-6 text-center py-12">
              <Network className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Explore Skills</h3>
              <p className="text-gray-600 mb-4">
                Enter a skill name above and choose a view to explore its relationships.
              </p>
            </CardContent>
          </Card>
          {allSkillsData && allSkillsData.skills.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Available Skills ({allSkillsData.count})</CardTitle>
                <CardDescription>Skills you can explore in the graph</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2 max-h-96 overflow-y-auto">
                  {allSkillsData.skills.map((s) => (
                    <Badge
                      key={s}
                      variant="outline"
                      className="cursor-pointer hover:bg-[#0077B5] hover:text-white transition-colors"
                      onClick={() => {
                        setSkill(s);
                        setViewMode('related');
                      }}
                    >
                      {s}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

